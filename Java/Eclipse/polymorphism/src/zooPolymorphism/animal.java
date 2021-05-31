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
	//final static int  m_threshold    = 30;  // DELME
	final static int    m_threshold	   = 90;
	final static int    g_threshold	   = 50;
	final static int    E_threshold	   = 70;
	static int          feedRunCount   = 0;
	static int          healthRunCount = 0;
	
	private int m_feed_rnum = 0;  // Monkey   specific feed random number range: 10 - 25
	private int g_feed_rnum = 0;  // Giraffe  specific feed random number range: 10 - 25
	private int e_feed_rnum = 0;  // Elephant specific feed random number range: 10 - 25
			
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
        setFeedValue(0);
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
	
	public abstract void 	setHealthRunCount(int count);
	
	public abstract int 	getHealthRunCount();
	
	public abstract int getThreshold();
	
	public abstract void setFeedValue(int val);
	
	public abstract int getFeedValue();
	
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
	
	public int getRandomValue(int min, int max) {
		return (int)(Math.random() * (((max - min) + 1)) + min);
	}
	
	/*
	 *  We don't want anyone in main() calling setRandomValues() as it should only 
	 *  be called once just before feeding the animals.  At the very least this method should be 
	 *  protected but my preference is private as this is an internal method that is not exposed
	 *  in derived classes.
	 */
	private void setRandomFeedValue() {
		
		m_feed_rnum = getRandomValue(10, 25);
		g_feed_rnum = getRandomValue(10, 25);
		e_feed_rnum = getRandomValue(10, 25);
		return;
	}
	
	public double getMrandomValue() {
		return (m_feed_rnum);
	}

	public double getGrandomValue() {
		return (g_feed_rnum);
	}

	public double getErandomValue() {
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
		
		if (obj.getStatus() == animal.DEAD) {
			return;
		} else if ( getStatus() == animal.LAME  &&	getCurrentHealth() < getThreshold()) {
			System.out.println("animal::changeStatus(): Status Changed from: " + getStatus() + " -> " + animal.DEAD + " for <" + getName() + ">");
			setStatus(animal.DEAD);
		} else if ( getStatus() == animal.LAME  &&	getCurrentHealth() > getThreshold()) {
			System.out.println("animal::changeStatus(): Status Changed from: " + getStatus() + " -> " + animal.HEALTHY + " for <" + getName() + ">");
			setStatus(animal.HEALTHY);
		} else if (getType() == animal.ELEPHANT && getCurrentHealth() < getThreshold()) {
			System.out.println("animal::changeStatus(): Status Changed from: " + getStatus() + " -> " + animal.LAME + " for <" + getName() + ">");
			setStatus(animal.LAME);			
		} else if (getCurrentHealth() < getThreshold()) {
			System.out.println("animal::changeStatus(): Status Changed from: " + getStatus() + " -> " + animal.DEAD + " for <" + getName() + ">");
			setStatus(animal.DEAD);
		} else {
			System.out.println("animal::changeStatus(): No change to status: <" + getStatus() + "> for <" + getName() + ">");
		}
	}
	
	public void feedAnimal() {
		if (getStatus() == DEAD)			
			return;
		
		// Generate and set the three feed random values
		setRandomFeedValue();
		
	}
	
	/*
	 * Each time this method is called it should generate a random number between 0 and 20 for each
	 * animal.  This value is passed to the appropriate animal whose health is then reduced by
	 * the percentage of their current health. 
	 */
	public int adjustHealthDown(animal obj, int value) {
		int ret = 0;
		
		if (obj.getStatus() == animal.DEAD) {
			return 0;
		}		
		//setHealthRunCount()
		float chealth = obj.getCurrentHealth();
		obj.setPrevHealth(chealth);
		float nhealth = (float) chealth - (chealth * value/100);
		setCurrentHealth(nhealth);		
		obj.changeStatus(obj);		
		return ret;
	}
	
	public void adjustHealthDownAllAnimals() {		
		animal.printBannerMsg("Adjusting health of animal down...");
		List<animal> myData = animal.getData();
		Iterator<animal> it = myData.listIterator();
		while (it.hasNext()) {
			animal obj = it.next();
			// Generate a random number for each animal between 0 and 20
			int val = getRandomValue(0, 20);
			obj.adjustHealthDown(obj, val);
		}
		return;
	}

	public void printInstanceAttributes(animal obj) {
		System.out.println(" Type:      <" + getType() + ">");
		System.out.println(" Name:      <" + getName() + ">");
		System.out.println(" Idx:       <" + getIdx() + ">");
		System.out.println(" Status:    <" + getStatus() + ">");
		System.out.println(" chealth:   <" + getCurrentHealth() + ">");
		System.out.println(" lhealth:   <" + getPrevHealth() + ">");
		System.out.println(" FeedValue: <" + getFeedValue() + ">");
		System.out.println("-------------------------------------------------------------------");
		return;
	}
	
	public void printAllInstanceAttributes() {
		animal.printBannerMsg("Printing attributes of all instances...");
		List<animal> myData = animal.getData();
		Iterator<animal> it = myData.listIterator();
		while (it.hasNext()) {
			animal obj = it.next();
			obj.printInstanceAttributes(obj);
		}
		return;
	}
}
