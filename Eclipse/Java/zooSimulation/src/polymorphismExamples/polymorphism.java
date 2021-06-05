package polymorphismExamples;

/*
 * Lakshman Brodie
 * October 2020
 *
 * A simple example to demonstrate polymorphism in  Java where class B is
 * extended by D1 and D2.  The C++ and Python versions of this example are
 * also available under my https://github.com/lab1301-git/src repository.
*/


import java.util.*;

public class polymorphism {
	private int flag;
	
	public polymorphism () {
		System.out.println("polymorphism() default ctor");
	}
	
	public polymorphism (int num) {
		System.out.println("polymorphism(int) ctor");
		flag=num;
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.println("Entered polymorphism..."); 
		int size;

		B b_obj = new D1();
		/*
		 *  getData() returns a read only container
		 */
		List<B> myData = b_obj.getData();

		System.out.println();
		size = b_obj.getSize();
		System.out.println("+++ List size=" + size);

		System.out.println("Loading data into Vector..."); 
		int idx=0;
		for (int i = 0; i < 5; i++) {
			idx = b_obj.getIdx();
		    B obj = new D1(idx);
		    b_obj.loadList(obj); 

			idx = b_obj.getIdx();
		    obj = new D2(idx);
		    b_obj.loadList(obj); 
		}

		System.out.println();
		size = b_obj.getSize();
		System.out.println("+++ List size=" + size);
	
	    B obj = new D1();
		System.out.println();
		try {
		    System.out.println(
		    "Testing whether we can insert an object into the read-only container myData..."
		    );
			myData.add(obj);
		} catch (UnsupportedOperationException e) {
		    System.out.println("** Caught UnsupportedOperationException on a READ ONLY collection**");
			System.out.println("** You do not have write permissions to myData container! **");
			System.out.println("** Use B::loadData() to load data. **");
		} 

		System.out.println();
		size = b_obj.getSize();
		System.out.println("Rechecking list size=" + size);
		
		System.out.println();
		System.out.println();
		System.out.println("Iterating around data collection....");

		/*
		 *  getIterator() returns a read only iterator
		 */
		Iterator<B> it = myData.iterator();
	    //Iterator<B> it = b_obj.getIterator();

		while(it.hasNext()) {
			B tmpObj = it.next();
			tmpObj.vfunc(); // vfunc() is polymorphic
		}
		
		System.out.println();
		it = myData.iterator();
		while(it.hasNext()) {
			B tmpObj = it.next();
		    try {
		    	/*
		    	 *  remove() below will throw an exception as myData is 
		    	 *  a read only container.
		    	 */
		    	System.out.println("Testing whether we can remove an object from the read only collection...");
		    	System.out.println();
			    it.remove();
		    } catch (UnsupportedOperationException e) {
		    	System.out.println("** Caught UnsupportedOperationException on a READ ONLY collection**");
			   	System.out.println("** You do not have write permissions to the data container! **");
			   	System.out.println("** Use B::loadData() to modify data. **");
			   	break;
		   	}
		} 
		
		System.out.println();
		size = b_obj.getSize();
		System.out.println("List size=" + size);
	} 
}
