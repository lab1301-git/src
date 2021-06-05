package polymorphismExamples;

/*
 * Lakshman Brodie
 * October 2020
 *
 * A simple example to demonstrate polymorphism in  Java where class B is
 * extended by D1 and D2.  The C++ and Python versions of this example are
 * also available under my https://github.com/lab1301-git/src repository.
*/


public class D1 extends B {
	private int seq;

	public D1() { System.out.println("D1::D1() ctor"); }

	public D1(int seq) {
		this.seq=seq;
		System.out.println("D1::D1(int) ctor.  Seq=" + seq);
	}
	
	public int getSeq() { return seq; }
	
	public void vfunc() {
		System.out.println("D1::vfunc().  Seq=" + getSeq()); 
	}

	public void func() { System.out.println("D1::func().  Seq=" + getSeq()); }
}
