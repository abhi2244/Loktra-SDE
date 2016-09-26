

import java.util.Scanner;

public class reverse_hash {

	/**
	 * @param args
	 */
	static String letters = "acdegilmnoprstuw";
  /*
    static long hash (String s) {
	    long h = 7;

	    for(int i = 0; i < s.length(); i++) {
	        h = (h * 37 + letters.indexOf(s.charAt(i)));
	    }
	    return h;
	}
*/	
	  public static String unhash(long n, int size) {
		    String result = "";
		    while (n>size) {
		      result = letters.charAt((int)(n%37)) + result;
		      n = n/37;
		    }
		    if (n != size) {
		    	return null;
		    }
		    else
		    	return result;
		  }
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner sc=new Scanner(System.in);
		long num=sc.nextLong();
		int size=sc.nextInt();
		String res=unhash(num,size);
		if(res==null){
			System.out.println("wrong combination, can't make word");
		}
		else
			System.out.println(unhash(num,size));
	}

}
