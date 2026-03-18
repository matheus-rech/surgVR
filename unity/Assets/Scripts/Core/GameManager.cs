using UnityEngine;

public class GameManager : MonoBehaviour
{
    public static GameManager Instance;

    private float startTime;
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
        if (!taskRunning && startTime == 0f)
        {
            return 0f;
        }
        return Time.time - startTime;
    }
}
