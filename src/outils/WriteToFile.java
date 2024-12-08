package outils;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;


public class WriteToFile {
    
    public void write(double value, long duration, int numIterations, int numProcessor, int nCible, double error){
        String outputFilePath = "output_G26_Assignment_"+ numIterations +".csv";
        //String outputFilePath = "output_G26_Pi.csv";
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
