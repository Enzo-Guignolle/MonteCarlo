package Assignment102;

// Estimate the value of Pi using Monte-Carlo Method, using parallel program

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;

import outils.WriteToFile;

class PiMonteCarlo {
	AtomicInteger nAtomSuccess;
	int nThrows;
	double value;
	int nProcessors;
	class MonteCarlo implements Runnable {
		@Override
		public void run() {
			double x = Math.random();
			double y = Math.random();
			if (x * x + y * y <= 1)
				nAtomSuccess.incrementAndGet();
		}
	}
	public PiMonteCarlo(int i, int nbProcessor) {
		this.nAtomSuccess = new AtomicInteger(0);
		this.nThrows = i;
		this.value = 0;
		this.nProcessors = nbProcessor;
	}
	public double getPi() {
		//int nProcessors = Runtime.getRuntime().availableProcessors();
		ExecutorService executor = Executors.newWorkStealingPool(nProcessors);
		for (int i = 1; i <= nThrows; i++) {
			Runnable worker = new MonteCarlo();
			executor.execute(worker);
		}
		executor.shutdown();
		while (!executor.isTerminated()) {
		}
		value = 4.0 * nAtomSuccess.get() / nThrows;
		return value;
	}
}
public class Assignment102 {
	public static void main(String[] args) {
		for (int i = 0; i<Integer.parseInt(args[0]); i++) {
			int nbIteration = 1000000;
			int nbProcessors = 16;
			PiMonteCarlo PiVal = new PiMonteCarlo(nbIteration, nbProcessors);
			long startTime = System.currentTimeMillis();
			double value = PiVal.getPi();
			long stopTime = System.currentTimeMillis();

			long duration = stopTime - startTime;
			int nCible = PiVal.nAtomSuccess.get();
			double error = (value - Math.PI) / Math.PI;

			WriteToFile writer = new WriteToFile();
			writer.write(value, duration, nbIteration, nbProcessors, nCible, error);

			System.out.println("Time Duration: " + duration + "ms");
			System.out.println("Total iteration: " + nbIteration);
			System.out.println("Available processors: " + nbProcessors);
			System.out.println("Nombre de success: " + PiVal.nAtomSuccess.get());
			System.out.println("Approx value:" + value);
			System.out.println("Error: " + (value - Math.PI) / Math.PI * 100 + " %\n");
		}
	}
}