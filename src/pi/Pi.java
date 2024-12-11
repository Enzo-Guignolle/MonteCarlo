package pi;

import outils.WriteToFile;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

/**
 * Approximates PI using the Monte Carlo method.  Demonstrates
 * use of Callables, Futures, and thread pools.
 */
public class Pi 
{
    public static void main(String[] args) throws Exception
	{
		for (int i = 0; i < Integer.parseInt(args[0]); i++) {
			int numWorker = 16;
			//int totalCount = 10000000 / numWorker;
			int totalCount = 10000000;
			long total = 0;
			// 10 workers, 50000 iterations each
			total = new Master().doRun(totalCount, numWorker);
			System.out.println("total from pi.Master = " + total);
		}
    }
}

/**
 * Creates workers to run the Monte Carlo simulation
 * and aggregates the results.
 */
class Master {
    public long doRun(int totalCount, int numWorkers) throws InterruptedException, ExecutionException
    {

	long startTime = System.currentTimeMillis();

	// Create a collection of tasks
	List<Callable<Long>> tasks = new ArrayList<Callable<Long>>();
	for (int i = 0; i < numWorkers; ++i) 
	    {
		tasks.add(new Worker(totalCount));
	    }
    
	// Run them and receive a collection of Futures
	ExecutorService exec = Executors.newFixedThreadPool(numWorkers);
	List<Future<Long>> results = exec.invokeAll(tasks);
	int total = 0;
    
	// Assemble the results.
	for (Future<Long> f : results)
	    {
		// Call to get() is an implicit barrier.  This will block
		// until result from corresponding worker is ready.
		total += f.get();
	    }
	double pi = 4.0 * total / totalCount / numWorkers;

	long stopTime = System.currentTimeMillis();
	double error =  (Math.abs((pi - Math.PI)) / Math.PI);
	WriteToFile writer = new WriteToFile();
	writer.write(pi, (stopTime - startTime), totalCount*numWorkers,numWorkers, total, error);

	System.out.println("\npi.Pi : " + pi );
	System.out.println("Time duration : " + (stopTime - startTime));
	System.out.println("Ntot: " + totalCount*numWorkers);
	System.out.println("Available processors: " + numWorkers);
	System.out.println("Nombre de points: " + total);
	System.out.println("Error: " + error +"\n");
	System.out.println("Différence : " + (pi - Math.PI));


	//System.out.println( (Math.abs((pi - Math.PI)) / Math.PI) +" "+ totalCount*numWorkers +" "+ numWorkers +" "+ (stopTime - startTime));

	exec.shutdown();
	return total;
    }
}

/**
 * Task for running the Monte Carlo simulation.
 */
class Worker implements Callable<Long> 
{   
    private long numIterations;
    public Worker(long num)
	{ 
	    this.numIterations = num; 
	}

  @Override
      public Long call() 
      {
	  long circleCount = 0;
	  Random prng = new Random ();
	  for (int j = 0; j < numIterations; j++) 
	      {
		  double x = prng.nextDouble();
		  double y = prng.nextDouble();
		  if ((x * x + y * y) < 1)  ++circleCount;
	      }
	  return circleCount;
      }
}
