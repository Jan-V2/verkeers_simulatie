using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEditor.Scripting.Python;

[CustomEditor(typeof(python_manager))]
public class python_manager_editor : Editor
{
    private python_manager targetManager;

    private void OnEndable()
    {
        targetManager = (python_manager) target;
    }

    public override void OnInspectorGUI()
    {
        if (GUILayout.Button("Launch Python Script", GUILayout.Height(35)))
        {
            //Debug.Log("This is working!");
            string path = Application.dataPath + "/Python/log_names.py";
            PythonRunner.RunFile(path);
        }
    }
}
