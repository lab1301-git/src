package zoo;

import java.util.*;
import java.util.stream.Stream;

public abstract class animal {
	private static Vector<animal> data = new Vector<animal>();
	
	Collection<animal> readOnlyData = Collections.unmodifiableCollection(data);

	final static String HEALTHY 	= "HEALTHY";
	final static String LIVE		= "LIVE";
	final static String DEAD		= "DEAD";
	final static String LAME		= "LAME";
	final static String MONKEY		= "Monkey";
	final static String GIRAFFE		= "Giraffe";
	final static String ELEPHANT	= "Elephant";
	final static String	DASH		= "-";
	final static float  m_threshold    = 30;	
	final static float  g_threshold	   = 50;
	final static float  e_threshold	   = 70;
	static int          gFeedRunCount   = 0;
	static int          gHealthRunCount = 0;
	
	private static int m_feed_rnum = 0;  // Monkey   specific feed random number range: 10 - 25
	private static int g_feed_rnum = 0;  // Giraffe  specific feed random number range: 10 - 25
	private static int e_feed_rnum = 0;  // Elephant specific feed random number range: 10 - 25
			
	protected String   evalName(String type, int idx) {
		return(type + DASH + idx);
	}
	
	protected void init(String type, int idx) {
		// Set initial status
        String name = evalName(type, idx);
        setName(name);
        setType(type);
        setStatus(HEALTHY); 
        setIdx(idx);
        setCurrentHealth(100);
        setPrevHealth(0);                
        return;
	}
	
	public abstract void 	setType(String type);
	
	public abstract String 	getType();
	
	public abstract void 	setName(String name);
	    	
	public abstract String 	getName();
	
	public abstract void 	setIdx(int idx);
	
	public abstract int 	getIdx();

	public abstract void   	setStatus(String status);
	
	public abstract String 	getStatus();
	
	public abstract void 	setCurrentHealth(float chealth);
	
	public abstract float 	getCurrentHealth();
	
	public abstract  void 	setPrevHealth(float chealth);
	
	public abstract float 	getPrevHealth();
	
	public abstract void 	setLocalHealthRunCount(int count);
	
	public abstract int 	getLocalHealthRunCount();
	
	public static int 	getGlobalFeedRunCount() {
		return (animal.gFeedRunCount);
	}
	
	public static int getGlobalHealthRunCount() {
		return (animal.gHealthRunCount);		
	}
	
	public abstract void 	setLocalFeedRunCount(int count);
		
	public abstract int 	getLocalFeedRunCount();
		
	public abstract float 	getThreshold();
	
	public abstract int 	getFeedRandomValue();
	
	public static void 		incrementFeedCount() {
		gFeedRunCount++;
		return;
	}
	
	public static void incrementHealthCount() {
		gHealthRunCount++;
		return;
	}
	
	public abstract void setFeedValue();
	
	public abstract float getFeedValue();
	
	/*
	public abstract animal animalFactory(int idx);  // Factory design pattern
	*/
		
	public static final void loadData(final animal obj) {
		data.add(obj);
		return;
	}
	
    /*
     *   List is an interface so we could also use an ArrayList,
     *   LinkedList or Stack here instead as they all also
     *   extend the List interface.  The variable data is private
     *   and is accessible only via loadData() & the read only
     *   getData() methods.
     */ 
	public static List<animal> getData() { return (Collections.unmodifiableList(data)); }
	
	public static Iterable<animal> getIterator() {
		return (Collections.unmodifiableList(data));
	}
	
	public Stream<animal> myData() {
		return data.stream();
	}
	
	public static animal getObject(int idx) {
		if (idx < 0) {
			idx = 0;
			String str = "animal::getObject(): Warning - Invalid negative index reset to 0!";
			printBannerMsg(str);			
		} else if (idx > data.size()) {
			String str = "animal::getObject(): Warning - Out of range index: <" + idx + "> " +
		                     "reset to: <" + (data.size() - 1) + ">";
				printBannerMsg(str);
			idx = data.size() - 1;
		}		
		return data.get(idx);
	}
	
	public static void printBannerMsg(String msg) {
	    System.out.println("*******************************************************************");
	    System.out.println("***** " + msg + " *****");
	    System.out.println("*******************************************************************");
	    return;
	}
	
	public static int getRandomValue(int min, int max) {
		return (int)(Math.random() * (((max - min) + 1)) + min);
	}
	
	/*
	 *  We don't want anyone in main() calling setRandomValues() as it should only 
	 *  be called once just before feeding the animals.  At the very least this method should be 
	 *  protected but my preference is private as this is an internal method that is not exposed
	 *  in derived classes.
	 */
	private static void setFeedRandomValues() {
		
		m_feed_rnum = getRandomValue(10, 25);
		g_feed_rnum = getRandomValue(10, 25);
		e_feed_rnum = getRandomValue(10, 25);
		return;
	}
	
		public int getMrandomValue() {
		return (m_feed_rnum);
	}

	public int getGrandomValue() {
		return (g_feed_rnum);
	}

	public int getErandomValue() {
		return (e_feed_rnum);
	}

	public void printRandomFeedValue() {
		System.out.println("****************** printRandomFeedValue() ******************");
	    System.out.println("Monkey   = <" + getMrandomValue() + ">");
	    System.out.println("Giraffe  = <" + getGrandomValue() + ">");
	    System.out.println("Elephant = <" + getErandomValue() + ">");	    
	    System.out.println("************************************************************");
	    return;
	}
	
	public void changeStatus(animal obj) {
		/*
		 * When an Elephant has a health below 70% it cannot walk. If its health does
		 * not return above 70% once the subsequent hour has elapsed, it is pronounced
		 * dead.
		 * When a Monkey has a health below 30%, or a Giraffe below 50%, it is
		 * pronounced dead straight away.
		 *		 		
		 * Set ret from Float.compare() by comparing two floats
		 *  ret > 0      chealth > threshold
		 *  ret < 0      chealth < threshold
		 *  ret = 0      chealth == threshold
		 */		
		
		int ret = Float.compare(obj.getCurrentHealth(), obj.getThreshold());
		
		if (obj.getStatus().equals(animal.DEAD)) {
			return;
		} else if ( obj.getStatus().equals(animal.LAME)  &&	ret < 0) {
			System.out.println("animal::changeStatus(): Status Changed from: " + getStatus() + " -> " + animal.DEAD + " for <" + getName() + ">");
			setStatus(animal.DEAD);
		} else if ( obj.getStatus().equals(animal.LAME)  &&	ret > 0) {
			System.out.println("animal::changeStatus(): Status Changed from: " + getStatus() + " -> " + animal.HEALTHY + " for <" + getName() + ">");
			obj.setStatus(animal.HEALTHY);
		} else if (getType().equals(animal.ELEPHANT) && ret < 0) {
			System.out.println("animal::changeStatus(): Status Changed from: " + getStatus() + " -> " + animal.LAME + " for <" + getName() + ">");
			obj.setStatus(animal.LAME);			
		} else if (ret < 0) {
			System.out.println("animal::changeStatus(): Status Changed from: " + getStatus() + " -> " + animal.DEAD + " for <" + getName() + ">");
			obj.setStatus(animal.DEAD);
		} else {
			System.out.println("animal::changeStatus(): No change to status: <" + getStatus() + "> for <" + getName() + "> (ret=" + ret + ")");
		}
	}
	
	public void feedAnimal(animal obj) {		
		if (obj.getStatus().equals(animal.DEAD))			
			return;
		
		int frun = getGlobalFeedRunCount();
		obj.setLocalFeedRunCount(frun);		
		obj.setFeedValue();  // set local feedValue to return by global animal specific random number
		/*
		 * Calculate new health for just fed animal using the animal specific random number
		*/
		int frnum = getFeedRandomValue();  // This returns the animal specific random number
		float chealth = obj.getCurrentHealth();  // Aptly named current health of animal instance
		obj.setPrevHealth(chealth);
		float nhealth = chealth + (chealth * (float) frnum/100);
		/*
		 * You can't have an nhealth > 100%
		 */
		float maxHealth = 100;
		if (Float.compare(nhealth, maxHealth) > 0) {
			nhealth = 100;
		}		
		obj.setCurrentHealth(nhealth);
		return;
	}
	
	public void feedAllAnimals() {
		
		animal.printBannerMsg("Feeding all animals...");
		/*
		* The user must be able to feed the animals in the zoo. When this happens,
		* the zoo should generate three random values between 10 and 25; one for each
		* type of animal.
		* Generate and set the three static feed random values via setRandomFeedValue().
		*/
		setFeedRandomValues();
		printRandomFeedValue();
		incrementFeedCount();
		/*
		 * Iterate around the data list and call feedAnimal()
		 */
		List<animal> myData = animal.getData();
		Iterator<animal> it = myData.listIterator();
		animal.incrementHealthCount();		
		while (it.hasNext()) {
			animal obj = it.next(); 
			feedAnimal(obj);
		}	
		//long deadAnimals = myData.parallelStream().filter(data -> (data.getStatus().count()));
		//long deadAnimals = myData.parallelStream().filter(string -> string.getStatus());
		return;
	}
	
	/*
	 * Each time adjustHealthDown() is called it should generate a random number between 0 and 20 for each
	 * animal.  This value is passed to the appropriate animal whose health is then reduced by
	 * the percentage of their current health. 
	 */
	public int adjustHealthDown(animal obj) {
		int ret = 0;
		
		if (obj.getStatus().equals(animal.DEAD)) {
			return 0;
		}
		
		/*
		 *  Every hour that passes, a random value between 0 and 20 is to be generated
		 *  for each animal.  This value should be passed to the appropriate animal, whose
		 *  health is then reduced by that percentage of their current health.
		 */
		
		int rvalue = animal.getRandomValue(0, 20);		
		int hrun   = animal.getGlobalHealthRunCount();
		obj.setLocalHealthRunCount(hrun);
		float chealth = obj.getCurrentHealth();
		obj.setPrevHealth(chealth);
		float nhealth = chealth - (chealth * (float) rvalue/100);		
		obj.setCurrentHealth(nhealth);		
		obj.changeStatus(obj);		
		return ret;
	}
	
	public void adjustHealthDownAllAnimals() {		
		printBannerMsg("Adjusting health of animal down...");
		List<animal> myData = animal.getData();
		Iterator<animal> it = myData.listIterator();
		animal.incrementHealthCount();
		
		while (it.hasNext()) {
			animal obj = it.next();
			obj.adjustHealthDown(obj);
		}
		return;
	}

	public void printInstanceAttributes(animal obj) {
		System.out.println(" Type:           <" + obj.getType() + ">");
		System.out.println(" Name:           <" + obj.getName() + ">");
		System.out.println(" Idx:            <" + obj.getIdx() + ">");
		System.out.println(" Status:         <" + obj.getStatus() + ">");
		System.out.println(" Current Health: <" + obj.getCurrentHealth() + ">     (Threshold: <" + obj.getThreshold() + ">)");
		System.out.println(" Prev Health:    <" + obj.getPrevHealth() + ">");
		System.out.println(" Health Runs:    <" + obj.getLocalHealthRunCount() + ">");
		System.out.println(" Feed Runs:      <" + obj.getLocalFeedRunCount() + ">");
		System.out.println(" Feed Value:     <" + obj.getFeedValue() + ">");		
		System.out.println("-------------------------------------------------------------------");
		return;
	}
	
	public void printAllInstanceAttributes() {
		animal.printBannerMsg("Printing attributes of all instances...");
		List<animal> myData = animal.getData();
		Iterator<animal> it = myData.listIterator();		
		while (it.hasNext()) {
			animal obj = it.next();			
			printInstanceAttributes(obj);
		}
		return;
	}
}
