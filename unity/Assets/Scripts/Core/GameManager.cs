using UnityEngine;

public class GameManager : MonoBehaviour
{
    public static GameManager Instance;

    public float startTime;
    public bool taskRunning;

    public TelemetryRecorder telemetry;
    public EventLogger eventLogger;

    void Awake()
    {
        if (Instance != null)
        {
            Debug.LogError("Multiple GameManager instances detected. Destroying duplicate.");
            Destroy(gameObject);
            return;
        }
        Instance = this;
    }

    public void StartTask()
    {
        startTime = Time.time;
        taskRunning = true;
    }

    public void EndTask()
    {
        taskRunning = false;

        string sessionId = System.DateTime.Now.ToString("yyyyMMdd_HHmmss");

        telemetry.Save(sessionId);
        eventLogger.Save(sessionId);
    }

    public float GetElapsedTime()
    {
        return Time.time - startTime;
    }
}
