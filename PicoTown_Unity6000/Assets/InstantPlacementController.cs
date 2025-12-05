using UnityEngine;
using Meta.XR;
using Meta.XR.MRUtilityKit;
using System.Collections.Generic;

public class InstantPlacementController : MonoBehaviour
{
    public Transform rightControllerAnchor;
    public GameObject prefabToPlace;
    public EnvironmentRaycastManager raycastManager;

    public DrawWithTrigger drawer;

    // private void Update()
    // {
    //     if (OVRInput.GetDown(OVRInput.RawButton.RIndexTrigger))
    //     {
    //         var ray = new Ray(
    //             rightControllerAnchor.position,
    //             rightControllerAnchor.forward
    //         );
    //         Debug.Log("Detected input, trying to place");
    //         TryPlace(ray);
    //     }
    // }

    // Adapted from https://developers.meta.com/horizon/documentation/unity/unity-mr-utility-kit-environment-raycast/
    public void TryPlace()
    {
        List<Vector3> points = drawer.points;
        if (!drawer.PointsValid())
        {
            Debug.LogWarning("Could not place building from drawing. Not enough points or points was null.");
            return;
        }

        // Use controller ray
        // var ray = new Ray(
        //     rightControllerAnchor.position,
        //     rightControllerAnchor.forward
        // );
        
        Vector3 rayStart = GetGroundCenter(points);
        Ray ray = new Ray(rayStart, Vector3.down);

        if (raycastManager.Raycast(ray, out var hit))
        {
            var objectToPlace = Instantiate(prefabToPlace);
            objectToPlace.transform.SetPositionAndRotation(
                hit.point,
                Quaternion.LookRotation(hit.normal, Vector3.up)
            );
            Debug.Log("Placed building");

            // If no MRUK component is present in the scene, we add an OVRSpatialAnchor component
            // to the instantiated prefab to anchor it in the physical space and prevent drift.
            if (MRUK.Instance?.IsWorldLockActive != true)
            {
                objectToPlace.AddComponent<OVRSpatialAnchor>();
            }
        }
    }

    // Gets the bounds the XZ plane of points and returns the center of the rectangular boundary
    //      - The returned y value is the max height of the points drawing
    public Vector3 GetGroundCenter(List<Vector3> points)
    {
        float minX = float.PositiveInfinity;
        float maxX = float.NegativeInfinity;
        float minZ = float.PositiveInfinity;
        float maxZ = float.NegativeInfinity;
        float maxY = float.NegativeInfinity;

        foreach (Vector3 p in points)
        {
            if (p.x < minX) minX = p.x;
            if (p.x > maxX) maxX = p.x;
            if (p.z < minZ) minZ = p.z;
            if (p.z > maxZ) maxZ = p.z;
            if (p.y > maxY) maxY = p.y;
        }

        float centerX = (minX + maxX) * 0.5f;
        float centerZ = (minZ + maxZ) * 0.5f;

        return new Vector3(centerX, maxY, centerZ);
    }
}