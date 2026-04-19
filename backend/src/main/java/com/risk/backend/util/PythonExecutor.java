package com.risk.backend.util;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class PythonExecutor {

    public static String runRag(String query) {
        String output = "";

        try {
            ProcessBuilder pb = new ProcessBuilder(
                    "python",
                    "rag/rag_engine.py",
                    query
            );

            Process process = pb.start();

            BufferedReader reader = new BufferedReader(
                    new InputStreamReader(process.getInputStream())
            );

            String line;
            while ((line = reader.readLine()) != null) {
                output += line + "\n";
            }

        } catch (Exception e) {
            e.printStackTrace();
        }

        return output;
    }
}