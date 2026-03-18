using UnityEngine;

public class CollisionTracker : MonoBehaviour
{
    public int collisionCount = 0;

    void OnCollisionEnter(Collision collision)
    {
        if (GameManager.Instance.taskRunning)
        {
            collisionCount++;
        }
    }
}
