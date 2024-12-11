package outils;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class WriteToFile {

    public void write(double value, long duration, int numIterations, int numProcessor, int nCible, double error) {
        String folderPath = "data"; 
        //String outputFilePath = folderPath + File.separator + "output_G26_Assignment_forte.csv";
        //String outputFilePath = folderPath + File.separator + "output_G26_Assignment_faible.csv";
        //String outputFilePath = folderPath + File.separator + "output_G26_Pi_forte.csv";
        String outputFilePath = folderPath + File.separator + "output_G26_Pi_faible.csv";

        File folder = new File(folderPath);
        if (!folder.exists()) {
            boolean folderCreated = folder.mkdirs();
            if (!folderCreated) {
                System.err.println("Erreur : Impossible de créer le dossier " + folderPath);
                return;
            }
        }

        File file = new File(outputFilePath);
        boolean fileExist = file.exists();

        String resultLine = String.format("%f;%dms;%d;%d;%d;%f\n", value, duration, numIterations, numProcessor, nCible, error);

        try (FileWriter writer = new FileWriter(outputFilePath, true)) {
            if (!fileExist) {
                writer.append("Pi;Duree;nbIteration;nbProcessor;nCible;Error\n");
            }
            writer.append(resultLine);
        } catch (IOException e) {
            System.err.println("Erreur: " + e.getMessage());
        }
    }
}
