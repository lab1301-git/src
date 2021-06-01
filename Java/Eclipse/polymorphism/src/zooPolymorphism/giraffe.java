package zoo;

public class giraffe extends animal {

	private String type;
	private String name;
	private int	   idx;
	private String status;
	private float  chealth;
	private float  lhealth;	
	private int    localFeedRunCount;
	private int    localHealthRunCount;
	private float  feedValue;
	
	giraffe(int idx) {
		System.out.println("giraffe::ctor(): Initialising instance: <" + idx + ">");
		init(animal.GIRAFFE, idx);		
	}
	
	public static animal animalFactory(int idx) {
		System.out.println("giraffe::animalFactory(): Returning new object: <" + idx + ">");
		return (new giraffe(idx));
	}
	
	public void setType(String type) {
		this.type = type;
		return;
	}
	
	public String getType() {
		return (this.type);
	}
	
	public float getThreshold() {
		return animal.g_threshold;
	}
	
	public void setName(String name) {
	    this.name = name;	
	    return;
	}
	
	public String getName() {
		return (this.name);
	}
	
	public void setIdx(int idx) {
		this.idx = idx;
		return;
	}
	
	public int getIdx() {
		return (this.idx);
	}
	
	public void   setStatus(final String status) {
		this.status = status;
		return;
	}
	
	public String getStatus() {
		return (this.status);
	}
	
	public void setCurrentHealth(float chealth) {		
		this.chealth = chealth;		
		return;
	}
	
	public float getCurrentHealth() {		
		return (this.chealth);
	}
	
	public void setPrevHealth(float chealth) {
		this.lhealth = chealth;
		return;
	}
	
	public float getPrevHealth() {
		return (this.lhealth);
	}
			
	public void setLocalHealthRunCount(int val) {
		this.localHealthRunCount = val;
		return;
	}
	
	public int getLocalHealthRunCount() {
		return (localHealthRunCount);
	}
	
	public int getLocalFeedRunCount() {
		return (localFeedRunCount);		
	}
	
	public void setLocalFeedRunCount(int frun) {
		this.localFeedRunCount = frun;				
		return;
	}
			
	public void setFeedValue() {
		this.feedValue = getGrandomValue();		
		return;
	}
	
	public float getFeedValue() {		
		return (feedValue);		
	}
	
	public int getFeedRandomValue() {
		return (getGrandomValue());
	}
	
}
