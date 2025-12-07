using UnityEngine;
using UnityEngine.Events;
using Meta.XR;
using Meta.XR.MRUtilityKit;
using System.Collections.Generic;


public class DrawWithTrigger : MonoBehaviour
{
    public Transform rightControllerAnchor;
    public LineRenderer lineRenderer;
    public List<Vector3> points;

    public UnityEvent OnConfirmDrawing;

    private void Update()
    {
        if (OVRInput.GetDown(OVRInput.RawButton.RIndexTrigger))
        {
            points.Clear();
            UpdateLineRenderer();
        }
        else if (OVRInput.Get(OVRInput.RawButton.RIndexTrigger))
        {
            UpdateLineRenderer();
        }
        else if (OVRInput.GetDown(OVRInput.RawButton.A))
        {
            OnFinishDraw();
            lineRenderer.positionCount = 0; // Don't clear points itself so we can use for calculations in building placement
        }
    }

    void UpdateLineRenderer()
    {
        points.Add(rightControllerAnchor.position);

        lineRenderer.positionCount = points.Count;
        lineRenderer.SetPositions(points.ToArray());
    }

    void OnFinishDraw()
    {
        if (PointsValid())
        {
            OnConfirmDrawing?.Invoke();
        }
    }

    public bool PointsValid()
    {
        return (points != null) && (points.Count >= 3); // Need enough points for a 2D rectangle on the xz (ground) axis
    }

    
}
