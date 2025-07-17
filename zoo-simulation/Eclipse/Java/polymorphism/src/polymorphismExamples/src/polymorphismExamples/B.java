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
import java.util.stream.*;

//import polymorphismExamples.polymorphism.B;

public abstract class B { 
	/*
	 *   List is an interface so we could also use an ArrayList,
	 *   LinkedList or Stack here instead as they all also
	 *   extend the List interface.  The variable data is private
	 *   and is accessible only via loadList() & the read only
	 *   getData() methods.
	 */
	private Vector<B> data = new Vector<B>();
	
	Collection<B> readOnlyData = Collections.unmodifiableCollection(data); 

	private static int idx = 0; 


	public B() { /*System.out.println("B::B() ctor");*/ }

	public int getIdx() { return ++idx; }

	public abstract void vfunc();

	public void func() { System.out.println("B::func()"); }

	public final void loadList(final B obj) {
		//System.out.println("loadList(B) called");
	    data.add(obj);
	}
	
	/*
	 * We make sure that data can't be modified by the caller.
	 */
	public List<B> getData() { return(Collections.unmodifiableList(data)); }

	/*
	 * We return a read only iterator.
	 */
	public Iterable<B> getIterator() { 
		return Collections.unmodifiableList(data);
	}
	
	/*
	 * Streams are Java 8 specific...
	 */
	public Stream<B> myData() {
		return data.stream();
	}
		
    public final int getSize() { return data.size(); }
}
