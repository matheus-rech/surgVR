using System.Collections.Generic;
using UnityEngine;
using System.IO;

[System.Serializable]
public class FrameData
{
    public float time;
    public Vector3 position;
    public Vector3 rotation;
    public float speed;
    public int collisions;
}

public class TelemetryRecorder : MonoBehaviour
{
    public Transform target;
    public CollisionTracker collisions;

    private List<FrameData> frames = new List<FrameData>();
    private Vector3 lastPos;

    void Start()
    {
        lastPos = target.position;
    }

    void Update()
    {
        if (!GameManager.Instance.taskRunning) return;

        float dt = Time.deltaTime;
        Vector3 pos = target.position;

        float speed = dt > 0f ? Vector3.Distance(pos, lastPos) / dt : 0f;

        frames.Add(new FrameData
        {
            time = GameManager.Instance.GetElapsedTime(),
            position = pos,
            rotation = target.eulerAngles,
            speed = speed,
            collisions = collisions.collisionCount
        });

        lastPos = pos;
    }

    public void Save(string sessionId)
    {
        string json = JsonUtility.ToJson(new Wrapper<FrameData>(frames), true);
        try
        {
            File.WriteAllText(Application.persistentDataPath + "/" + sessionId + "_telemetry.json", json);
        }
        catch (System.Exception e)
        {
            Debug.LogError($"Failed to save telemetry for session {sessionId}: {e.Message}");
        }
    }
}

[System.Serializable]
public class Wrapper<T>
{
    public List<T> items;
    public Wrapper(List<T> items) { this.items = items; }
}
