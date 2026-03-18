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
    [System.Serializable]
    private class EventListWrapper
    {
        public List<Event> events;

        public EventListWrapper(List<Event> events)
        {
            this.events = events;
        }
    }

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
        string json = JsonUtility.ToJson(new EventListWrapper(events), true);
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
