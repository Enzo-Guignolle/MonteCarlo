package distributedMC_step1_javaSocket.pi;

/**
 * Approximates PI using the Monte Carlo method.  Demonstrates
 * use of Callables, Futures, and thread pools.
 */
public class Pi 
{
    public static long main(String[] args) throws Exception
    {
		long total=0;
		// 10 workers, 50000 iterations each
		total = new Master().doRun(50000, 10);
		System.out.println("total from Master = " + total);
		return total;
    }
}

