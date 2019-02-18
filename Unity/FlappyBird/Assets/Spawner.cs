using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Spawner : MonoBehaviour
{
    public float spawnRate = 3f;
    public GameObject obstacle;

    // Start is called before the first frame update
    void Start()
    {
        InvokeRepeating("spawnObstacle", 0, spawnRate);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void spawnObstacle()
    {
        float y = Random.Range(0, 25);
        Vector3 position = new Vector3(transform.position.x, 30 - y, transform.position.z);
        GameObject hindernis = Instantiate(obstacle, position, Quaternion.identity);
        Destroy(hindernis, 5);
    }
}
