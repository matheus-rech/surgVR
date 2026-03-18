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
        if (telemetry != null) telemetry.Clear();
        if (eventLogger != null) eventLogger.Clear();
        startTime = Time.time;
        taskRunning = true;
    }

    public void EndTask()
    {
        taskRunning = false;

        string sessionId = System.DateTime.Now.ToString("yyyyMMdd_HHmmss");

        if (telemetry == null || eventLogger == null)
        {
            Debug.LogError("GameManager.EndTask: telemetry and/or eventLogger are not assigned. Please assign them in the inspector.");
            return;
        }

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
