/***********************************************************************************************
* Author:      Lakshman Brodie - 1st June 2021   (lab1301)
* Date:        24th May 2021
* 
* Description: The code addresses the following specification:
*
* Write a simple Zoo simulator which contains 3 different types of animals:
*  monkey,
*  giraffe
*  elephant
*
* The zoo should open with 5 of each type of animal.
* Each animal has a health value held as a percentage (100% is completely
* healthy)
* Every animal starts at 100% health. This value should be a floating point
* value.
*
* The application should act as a simulator, with time passing at the rate of
* 1 hour with each iteration. Every hour that passes, a random value between 0
* and 20 is to be generated for each animal. This value should be passed to
* the appropriate animal, whose health is then reduced by that percentage of
* their current health.
*
* The user must be able to feed the animals in the zoo. When this happens,
* the zoo should generate three random values between 10 and 25; one for each
* type of animal. The health of the respective animals is to be increased by
* the specified percentage of their current health. Health should be capped
* at 100%.
*
* When an Elephant has a health below 70% it cannot walk. If its health does
* not return above 70% once the subsequent hour has elapsed, it is pronounced
* dead.
* When a Monkey has a health below 30%, or a Giraffe below 50%, it is
* pronounced dead straight away.
*
* This program demonstrates the OO "Is a" relationship via polymorphisim.
*
***********************************************************************************************/

package zoo;

import java.util.*;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.ZoneId;

public class zoo {
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
				
		System.out.println("Java version:    <" + System.getProperty("java.version") + ">");
		System.out.println("Java VM Version: <"+System.getProperty("java.vm.version") + ">");
		System.out.println();
		animal.printBannerMsg("Starting zoo simulation");
		
		/*
		 * Load list with animal objects
		 */
		System.out.println();
		animal.printBannerMsg("Loading animal objects into data list...");
		int i = 0;
		while (i++ < 5) {
			animal.loadData(monkey.animalFactory(i));			
		}		
		
		List<animal> myData = animal.getData();
		Iterator<animal> it = myData.listIterator();
		
		System.out.println();
				
		/**************
		animal.printBannerMsg("Iterating around data conatainer...");
		while (it.hasNext()) {
			animal obj = it.next();
			obj.printInstanceAttributes();
			
			obj.adjustHealthDown();
		}
		*/
		
		// get the first/any object from container
		animal obj = animal.getObject(1);
		obj.printAllInstanceAttributes();
		
		obj.adjustHealthDownAllAnimals();
		System.out.println();
		obj.printAllInstanceAttributes();
		
		obj.adjustHealthDownAllAnimals();
		System.out.println();
		obj.printAllInstanceAttributes();
		
		obj.feedAllAnimals();
		System.out.println();
		obj.printAllInstanceAttributes();
		
		System.exit(0);
	}    
}
