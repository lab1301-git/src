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
*/

package main

import (
	"fmt"
	"math/rand"
	"time"
)

// Animal interface
type Animal interface {
	ID() int
	Name() string
	Health() float64
	IsDead() bool
	ApplyDamage(percent float64)
	Heal(percent float64)
	UpdateStatus()
	Description()
}

// Monkey struct
type Monkey struct {
	id     int
	health float64
	dead   bool
}

func NewMonkey(id int) *Monkey {
	return &Monkey{id: id, health: 100.0, dead: false}
}

func (m *Monkey) ID() int             { return m.id }
func (m *Monkey) Name() string        { return "Monkey" }
func (m *Monkey) Health() float64     { return m.health }
func (m *Monkey) IsDead() bool        { return m.dead }
func (m *Monkey) ApplyDamage(percent float64) {
	if !m.dead {
		m.health -= m.health * (percent / 100.0)
		if m.health < 0 {
			m.health = 0
		}
		m.UpdateStatus()
	}
}
func (m *Monkey) Heal(percent float64) {
	if !m.dead {
		m.health += m.health * (percent / 100.0)
		if m.health > 100 {
			m.health = 100
		}
	}
}
func (m *Monkey) UpdateStatus() {
	if m.health < 30 {
		m.dead = true
	}
}
func (m *Monkey) Description() {
	if m.dead {
		fmt.Printf("Monkey #%d is dead.\n", m.id)
	} else {
		fmt.Printf("Monkey #%d has %.1f%% health.\n", m.id, m.health)
	}
}

// Giraffe struct
type Giraffe struct {
	id     int
	health float64
	dead   bool
}

func NewGiraffe(id int) *Giraffe {
	return &Giraffe{id: id, health: 100.0, dead: false}
}

func (g *Giraffe) ID() int             { return g.id }
func (g *Giraffe) Name() string        { return "Giraffe" }
func (g *Giraffe) Health() float64     { return g.health }
func (g *Giraffe) IsDead() bool        { return g.dead }
func (g *Giraffe) ApplyDamage(percent float64) {
	if !g.dead {
		g.health -= g.health * (percent / 100.0)
		if g.health < 0 {
			g.health = 0
		}
		g.UpdateStatus()
	}
}
func (g *Giraffe) Heal(percent float64) {
	if !g.dead {
		g.health += g.health * (percent / 100.0)
		if g.health > 100 {
			g.health = 100
		}
	}
}

func (g *Giraffe) UpdateStatus() {
	if g.health < 50 {
		g.dead = true
	}
}
func (g *Giraffe) Description() {
	if g.dead {
		fmt.Printf("Giraffe #%d is dead.\n", g.id)
	} else {
		fmt.Printf("Giraffe #%d has %.1f%% health.\n", g.id, g.health)
	}
}

// Elephant struct
type Elephant struct {
	id     int
	health float64
	dead   bool
	atRisk bool
}

func NewElephant(id int) *Elephant {
	return &Elephant{id: id, health: 100.0, dead: false, atRisk: false}
}

func (e *Elephant) ID() int             { return e.id }
func (e *Elephant) Name() string        { return "Elephant" }
func (e *Elephant) Health() float64     { return e.health }
func (e *Elephant) IsDead() bool        { return e.dead }
func (e *Elephant) ApplyDamage(percent float64) {
	if !e.dead {
		e.health -= e.health * (percent / 100.0)
		if e.health < 0 {
			e.health = 0
		}
		e.UpdateStatus()
	}
}
func (e *Elephant) Heal(percent float64) {
	if !e.dead {
		e.health += e.health * (percent / 100.0)
		if e.health > 100 {
			e.health = 100
		}
	}
}
func (e *Elephant) UpdateStatus() {
	if e.health < 70 {
		if e.atRisk {
			e.dead = true
		} else {
			fmt.Printf("Elephant #%d is too weak to walk!\n", e.id)
			e.atRisk = true
		}
	} else {
		e.atRisk = false
	}
}
func (e *Elephant) Description() {
	if e.dead {
		fmt.Printf("Elephant #%d is dead.\n", e.id)
	} else {
		fmt.Printf("Elephant #%d has %.1f%% health.\n", e.id, e.health)
	}
}

// Zoo struct
type Zoo struct {
	animals []Animal
}

func NewZoo() *Zoo {
	var animals []Animal
	id := 1
	for i := 0; i < 5; i++ {
		animals = append(animals, NewMonkey(id))
		id++
		animals = append(animals, NewGiraffe(id))
		id++
		animals = append(animals, NewElephant(id))
		id++
	}
	return &Zoo{animals: animals}
}

func (z *Zoo) ShowAnimals() {
	for _, a := range z.animals {
		a.Description()
	}
}

func (z *Zoo) SimulateHour(hour int) {
	fmt.Printf("\n--- Hour %d ---\n", hour)
	for _, a := range z.animals {
		if a.IsDead() {
			a.Description()
			continue
		}
		damage := rand.Float64()*20.0 // 0–20%
		a.ApplyDamage(damage)
		fmt.Printf("%s #%d took %.1f%% damage.\n", a.Name(), a.ID(), damage)
		a.Description()
	}
}

func (z *Zoo) FeedAnimals() {
	monkeyBoost := 10 + rand.Float64()*15 // 10–25%
	giraffeBoost := 10 + rand.Float64()*15
	elephantBoost := 10 + rand.Float64()*15

	fmt.Printf("\nFeeding animals: Monkeys +%.1f%%, Giraffes +%.1f%%, Elephants +%.1f%%\n",
		monkeyBoost, giraffeBoost, elephantBoost)

	for _, a := range z.animals {
		if a.IsDead() {
			a.Description()
			continue
		}
		switch a.Name() {
		case "Monkey":
			a.Heal(monkeyBoost)
		case "Giraffe":
			a.Heal(giraffeBoost)
		case "Elephant":
			a.Heal(elephantBoost)
		}
		a.Description()
	}
}

// Main function
func main() {
	rand.Seed(time.Now().UnixNano())
	zoo := NewZoo()

	for hour := 1; hour <= 10; hour++ {
		zoo.SimulateHour(hour)
		if hour%3 == 0 {
			zoo.FeedAnimals()
		}
	}
}
