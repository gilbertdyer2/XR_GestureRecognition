using UnityEngine;
using Meta.XR;
using Meta.XR.MRUtilityKit;

public class InstantPlacementController : MonoBehaviour
{
    public Transform rightControllerAnchor;
    public GameObject prefabToPlace;
    public EnvironmentRaycastManager raycastManager;

    private void Update()
    {
        if (OVRInput.GetDown(OVRInput.RawButton.RIndexTrigger))
        {
            var ray = new Ray(
                rightControllerAnchor.position,
                rightControllerAnchor.forward
            );

            TryPlace(ray);
        }
    }

    private void TryPlace(Ray ray)
    {
        if (raycastManager.Raycast(ray, out var hit))
        {
            var objectToPlace = Instantiate(prefabToPlace);
            objectToPlace.transform.SetPositionAndRotation(
                hit.point,
                Quaternion.LookRotation(hit.normal, Vector3.up)
            );

            // If no MRUK component is present in the scene, we add an OVRSpatialAnchor component
            // to the instantiated prefab to anchor it in the physical space and prevent drift.
            if (MRUK.Instance?.IsWorldLockActive != true)
            {
                objectToPlace.AddComponent<OVRSpatialAnchor>();
            }
        }
    }
}