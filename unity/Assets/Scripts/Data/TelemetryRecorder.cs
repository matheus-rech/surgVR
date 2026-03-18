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

    void Awake()
    {
        if (target == null)
        {
            Debug.LogError("TelemetryRecorder: target Transform is not assigned!", this);
            enabled = false;
            return;
        }
        if (collisions == null)
        {
            Debug.LogError("TelemetryRecorder: CollisionTracker is not assigned!", this);
            enabled = false;
            return;
        }
        lastPos = target.position;
    }

#if UNITY_EDITOR
    void OnValidate()
    {
        if (target == null)
            Debug.LogWarning("TelemetryRecorder: target Transform is not assigned!", this);
        if (collisions == null)
            Debug.LogWarning("TelemetryRecorder: CollisionTracker is not assigned!", this);
    }
#endif

    void Update()
    {
        if (GameManager.Instance == null || !GameManager.Instance.taskRunning || target == null || collisions == null) return;

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

    public void Clear()
    {
        frames.Clear();
        if (target != null)
            lastPos = target.position;
        if (collisions != null)
            collisions.Clear();
    }

    public void Save(string sessionId)
    {
        string json = JsonUtility.ToJson(new Wrapper<FrameData>(frames), true);
        try
        {
            string sessionDirectory = Path.Combine(Application.persistentDataPath, sessionId);
            Directory.CreateDirectory(sessionDirectory);
            string telemetryPath = Path.Combine(sessionDirectory, "telemetry.json");
            File.WriteAllText(telemetryPath, json);
        }
        catch (System.Exception e)
        {
            Debug.LogError($"Failed to save telemetry for session {sessionId}: {e.Message}");
        }
    }
}

