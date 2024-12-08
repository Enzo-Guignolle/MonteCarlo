package distributedMC_step1_javaSocket.pi;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*; /**
 * Creates workers to run the Monte Carlo simulation
 * and aggregates the results.
 */
public class Master {
    public long doRun(long totalCount, int numWorkers) throws InterruptedException, ExecutionException
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
	long total = 0;
    
	// Assemble the results.
	for (Future<Long> f : results)
	    {
		// Call to get() is an implicit barrier.  This will block
		// until result from corresponding worker is ready.
		total += f.get();
	    }
	double pi = 4.0 * total / totalCount / numWorkers;

	long stopTime = System.currentTimeMillis();
	//double error = (Math.abs((pi - Math.PI)) / Math.PI);

	//WriteToFile writer = new WriteToFile();
	//writer.write(pi, (stopTime - startTime), totalCount*numWorkers, numWorkers, total, error);
	
	System.out.println("\npi.Pi : " + pi );
	System.out.println("Time Duration (ms): " + (stopTime - startTime));
	System.out.println("Ntot: " + totalCount*numWorkers);
	System.out.println("Available processors: " + numWorkers);
	System.out.println("Nombre de point compté: " + total);
	System.out.println("Error: " + (Math.abs((pi - Math.PI)) / Math.PI));
	System.out.println("Difference to exact value of pi: " + (pi - Math.PI) + "\n");
	
	//System.out.println( (Math.abs((pi - Math.PI)) / Math.PI) +" "+ totalCount*numWorkers +" "+ numWorkers +" "+ (stopTime - startTime));
	exec.shutdown();
	return total;
    }
}
