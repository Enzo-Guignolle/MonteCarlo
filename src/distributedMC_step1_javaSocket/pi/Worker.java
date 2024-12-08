package distributedMC_step1_javaSocket.pi;

import java.util.Random;
import java.util.concurrent.Callable; /**
 * Task for running the Monte Carlo simulation.
 */
public class Worker implements Callable<Long> 
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
	  for (long j = 0; j < numIterations; j++)
	      {
		  double x = prng.nextDouble();
		  double y = prng.nextDouble();
		  if ((x * x + y * y) < 1)  ++circleCount;
	      }
	  return circleCount;
      }
}
