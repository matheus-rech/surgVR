using System.Collections.Generic;
using UnityEngine;
using System.IO;

[System.Serializable]
public class Event
{
    public string name;
    public float time;
}

public class EventLogger : MonoBehaviour
{
    private List<Event> events = new List<Event>();

    public void Log(string eventName)
    {
        if (GameManager.Instance == null)
        {
            Debug.LogError("EventLogger: GameManager.Instance is null. Cannot log event.");
            return;
        }
        events.Add(new Event
        {
            name = eventName,
            time = GameManager.Instance.GetElapsedTime()
        });
    }

    public void Save(string sessionId)
    {
        string json = JsonUtility.ToJson(new Wrapper<Event>(events), true);
        try
        {
            File.WriteAllText(Application.persistentDataPath + "/" + sessionId + "_events.json", json);
        }
        catch (System.Exception e)
        {
            Debug.LogError($"Failed to save events for session {sessionId}: {e.Message}");
        }
    }
}
