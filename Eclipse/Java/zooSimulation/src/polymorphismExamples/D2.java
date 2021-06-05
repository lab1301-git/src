package polymorphismExamples;

/*
 * Lakshman Brodie
 * October 2020
 *
 * A simple example to demonstrate polymorphism in  Java where class B is
 * extended by D1 and D2.  The C++ and Python versions of this example are
 * also available under my https://github.com/lab1301-git/src repository.
*/


public class D2 extends B {
	private int seq;

	public D2() { System.out.println("D2::D2() ctor"); } 

	public D2(int seq) {
		this.seq=seq;
		System.out.println("D2::D2(int) ctor.  Seq=" + seq);
	} 
	
	public int getSeq() { return seq; }

	public void vfunc() { System.out.println("D2::vfunc().  Seq=" + getSeq()); }

	public void func() { System.out.println("D2::func()"); }
}
