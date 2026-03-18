using System.Collections.Generic;
using UnityEngine;
using System.IO;

[System.Serializable]
public class TaskEvent
{
    public string name;
    public float time;
}

public class EventLogger : MonoBehaviour
{
    private List<TaskEvent> events = new List<TaskEvent>();

    public void Log(string eventName)
    {
        if (GameManager.Instance == null)
        {
            Debug.LogError("EventLogger: GameManager.Instance is null. Cannot log event.");
            return;
        }
        events.Add(new TaskEvent
        {
            name = eventName,
            time = GameManager.Instance.GetElapsedTime()
        });
    }

    public void Clear()
    {
        events.Clear();
    }

    public void Save(string sessionId)
    {
        string json = JsonUtility.ToJson(new Wrapper<TaskEvent>(events), true);
        try
        {
            string sessionDirectory = Path.Combine(Application.persistentDataPath, sessionId);
            Directory.CreateDirectory(sessionDirectory);

            string filePath = Path.Combine(sessionDirectory, "events.json");
            File.WriteAllText(filePath, json);
        }
        catch (System.Exception e)
        {
            Debug.LogError($"Failed to save events for session {sessionId}: {e.Message}");
        }
    }
}
