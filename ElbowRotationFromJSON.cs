using UnityEngine;
using UnityEngine.Networking;
using System.Collections;

public class ElbowRotationFromJSON : MonoBehaviour
{
    public string jsonUrl = "http://localhost:8000/elbow_angle.json";
    private float currentAngle = 0f;
    private float targetAngle = 0f;
    public float rotationSpeed = 180f;
    public float rotationOffset = 0f;

    void Start()
    {
        StartCoroutine(FetchAngleLoop());
    }

    void Update()
    {
        currentAngle = Mathf.MoveTowardsAngle(currentAngle, targetAngle, rotationSpeed * Time.deltaTime);
        transform.localRotation = Quaternion.Euler(0f, 0f, currentAngle + rotationOffset);
    }

    IEnumerator FetchAngleLoop()
    {
        while (true)
        {
            UnityWebRequest www = UnityWebRequest.Get(jsonUrl);
            www.SetRequestHeader("Cache-Control", "no-cache");
            www.SetRequestHeader("Pragma", "no-cache");

            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.Success)
            {
                string jsonText = www.downloadHandler.text;
                try
                {
                    AngleData data = JsonUtility.FromJson<AngleData>(jsonText);
                    float rawAngle = data.angle;
                    targetAngle = (rawAngle % 360 + 360) % 360;
                }
                catch (System.Exception e)
                {
                    Debug.LogWarning("Failed to parse JSON: " + e.Message);
                }
            }

            yield return new WaitForSeconds(0.05f);
        }
    }
}
