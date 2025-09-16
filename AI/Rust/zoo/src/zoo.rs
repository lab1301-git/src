/*
 * Lakshman Brodie
 * September 2025
 *
 * AI has been used to generate boilerplate code to enhance productivity when migrating
 * the zoo simulation to Rust.
 *
 * The code addresses the following specification: 
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
*/

use rand::Rng;

// Base trait
trait Animal {
    fn id(&self) -> usize;
    fn name(&self) -> &'static str;
    fn health(&self) -> f32;
    fn is_dead(&self) -> bool;
    fn apply_damage(&mut self, percent: f32);
    fn heal(&mut self, percent: f32);
    fn update_status(&mut self);

    fn description(&self) {
        if self.is_dead() {
            println!("{} #{} is dead.", self.name(), self.id());
        } else {
            println!(
                "{} #{} has {:.1}% health.",
                self.name(),
                self.id(),
                self.health()
            );
        }
    }
}

// Monkey struct
struct Monkey {
    id: usize,
    health: f32,
    dead: bool,
}

impl Monkey {
    fn new(id: usize) -> Self {
        Monkey {
            id,
            health: 100.0,
            dead: false,
        }
    }
}

impl Animal for Monkey {
    fn id(&self) -> usize {
        self.id
    }
    fn name(&self) -> &'static str {
        "Monkey"
    }
    fn health(&self) -> f32 {
        self.health
    }
    fn is_dead(&self) -> bool {
        self.dead
    }
    fn apply_damage(&mut self, percent: f32) {
        if !self.dead {
            self.health -= self.health * (percent / 100.0);
            if self.health < 0.0 {
                self.health = 0.0;
            }
            self.update_status();
        }
    }
    fn heal(&mut self, percent: f32) {
        if !self.dead {
            self.health += self.health * (percent / 100.0);
            if self.health > 100.0 {
                self.health = 100.0;
            }
        }
    }
    fn update_status(&mut self) {
        if self.health < 30.0 {
            self.dead = true;
        }
    }
}

// Giraffe struct
struct Giraffe {
    id: usize,
    health: f32,
    dead: bool,
}

impl Giraffe {
    fn new(id: usize) -> Self {
        Giraffe {
            id,
            health: 100.0,
            dead: false,
        }
    }
}

impl Animal for Giraffe {
    fn id(&self) -> usize {
        self.id
    }
    fn name(&self) -> &'static str {
        "Giraffe"
    }
    fn health(&self) -> f32 {
        self.health
    }
    fn is_dead(&self) -> bool {
        self.dead
    }
    fn apply_damage(&mut self, percent: f32) {
        if !self.dead {
            self.health -= self.health * (percent / 100.0);
            if self.health < 0.0 {
                self.health = 0.0;
            }
            self.update_status();
        }
    }
    fn heal(&mut self, percent: f32) {
        if !self.dead {
            self.health += self.health * (percent / 100.0);
            if self.health > 100.0 {
                self.health = 100.0;
            }
        }
    }
    fn update_status(&mut self) {
        if self.health < 50.0 {
            self.dead = true;
        }
    }
}

// Elephant struct
struct Elephant {
    id: usize,
    health: f32,
    dead: bool,
    at_risk: bool,
}

impl Elephant {
    fn new(id: usize) -> Self {
        Elephant {
            id,
            health: 100.0,
            dead: false,
            at_risk: false,
        }
    }
}

impl Animal for Elephant {
    fn id(&self) -> usize {
        self.id
    }
    fn name(&self) -> &'static str {
        "Elephant"
    }
    fn health(&self) -> f32 {
        self.health
    }
    fn is_dead(&self) -> bool {
        self.dead
    }
    fn apply_damage(&mut self, percent: f32) {
        if !self.dead {
            self.health -= self.health * (percent / 100.0);
            if self.health < 0.0 {
                self.health = 0.0;
            }
            self.update_status();
        }
    }
    fn heal(&mut self, percent: f32) {
        if !self.dead {
            self.health += self.health * (percent / 100.0);
            if self.health > 100.0 {
                self.health = 100.0;
            }
        }
    }
    fn update_status(&mut self) {
        if self.health < 70.0 {
            if self.at_risk {
                // Was already at risk last hour
                self.dead = true;
            } else {
                println!("Elephant #{} is too weak to walk!", self.id);
                self.at_risk = true;
            }
        } else {
            self.at_risk = false;
        }
    }
}

// Zoo struct
struct Zoo {
    animals: Vec<Box<dyn Animal>>,
}

impl Zoo {
    fn new() -> Self {
        let mut animals: Vec<Box<dyn Animal>> = Vec::new();
        let mut id_counter: usize = 1;

        for _ in 0..5 {
            animals.push(Box::new(Monkey::new(id_counter)));
            id_counter += 1;
            animals.push(Box::new(Giraffe::new(id_counter)));
            id_counter += 1;
            animals.push(Box::new(Elephant::new(id_counter)));
            id_counter += 1;
        }

        Zoo { animals }
    }

    fn show_animals(&self) {
        for animal in &self.animals {
            animal.description();
        }
    }

    fn simulate_hour(&mut self, hour: usize) {
        println!("\n--- Hour {} ---", hour);
        let mut rng = rand::rng();

        for animal in self.animals.iter_mut() {
            if animal.is_dead() {
                animal.description();
                continue;
            }
            let damage_percent: f32 = rng.random_range(0.0..=20.0);
            animal.apply_damage(damage_percent);
            println!(
                "{} #{} took {:.1}% damage.",
                animal.name(),
                animal.id(),
                damage_percent
            );
            animal.description();
        }
    }

    fn feed_animals(&mut self) {
        let mut rng = rand::rng();

        let monkey_boost = rng.random_range(10.0..=25.0);
        let giraffe_boost = rng.random_range(10.0..=25.0);
        let elephant_boost = rng.random_range(10.0..=25.0);

        println!(
            "\nFeeding animals: Monkeys +{:.1}%, Giraffes +{:.1}%, Elephants +{:.1}%",
            monkey_boost, giraffe_boost, elephant_boost
        );

        for animal in self.animals.iter_mut() {
                if animal.is_dead() {
                    animal.description();
                    continue;
                }

                match animal.name() {
                    "Monkey" => animal.heal(monkey_boost),
                    "Giraffe" => animal.heal(giraffe_boost),
                    "Elephant" => animal.heal(elephant_boost),
                    _ => {}
            }
            animal.description();
        }
    }
}

fn main() {
    let mut zoo = Zoo::new();

    for hour in 1..=10 {
        zoo.simulate_hour(hour);

        if hour % 3 == 0 {
            // Feed every 3 hours
            zoo.feed_animals();
        }
    }
    zoo.show_animals();
}


