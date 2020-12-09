use std::collections::HashSet;
use std::convert::TryFrom;
use std::io::{self, BufRead};

struct Runtime<'a> {
    instructions: &'a Vec<Instruction>,
    pub accumulator: isize,
    ins_index: usize,
}

#[derive(std::cmp::PartialEq, Copy, Clone)]
enum InsType {
    Acc,
    Jmp,
    Nop,
}

#[derive(Copy, Clone)]
struct Instruction {
    instruction_type: InsType,
    number: isize,
}

impl Instruction {
    pub fn flipped_jmp_nop(&self) -> Self {
        match self.instruction_type {
            InsType::Acc => panic!("Tried to toggle an acc instruction"),
            InsType::Jmp => Self {
                instruction_type: InsType::Nop,
                number: self.number,
            },
            InsType::Nop => Self {
                instruction_type: InsType::Jmp,
                number: self.number,
            },
        }
    }
}

impl<'a> Runtime<'a> {
    pub fn run(&mut self) -> Result<(), &'static str> {
        let mut instructions_run = HashSet::<usize>::new();

        while !instructions_run.contains(&self.ins_index) {
            instructions_run.insert(self.ins_index);

            if let Some(instruction) = self.instructions.get(self.ins_index) {
                match instruction {
                    Instruction {
                        instruction_type: InsType::Acc,
                        number,
                    } => {
                        self.accumulator += *number;
                        self.ins_index += 1;
                    }
                    Instruction {
                        instruction_type: InsType::Jmp,
                        number,
                    } => {
                        self.ins_index =
                            usize::try_from(isize::try_from(self.ins_index).unwrap() + *number)
                                .unwrap();
                    }
                    Instruction {
                        instruction_type: InsType::Nop,
                        number: _,
                    } => {
                        self.ins_index += 1;
                    }
                }
            } else {
                return Ok(());
            }
        }

        Err("Program finished in an infinite loop")
    }
}

fn main() {
    let stdin = io::stdin();
    let instructions = stdin
        .lock()
        .lines()
        .map(|elem| {
            let line = elem.unwrap();
            let mut line_chunks = line.split(" ");
            let instruction_type = match line_chunks.next() {
                Some("acc") => InsType::Acc,
                Some("jmp") => InsType::Jmp,
                Some("nop") => InsType::Nop,
                Some(other) => panic!("Unrecognized instruction {}", other),
                None => panic!("Empty instruction"),
            };

            Instruction {
                instruction_type,
                number: isize::from_str_radix(line_chunks.next().unwrap(), 10).unwrap(),
            }
        })
        .collect();

    let mut runtime1 = Runtime {
        instructions: &instructions,
        accumulator: 0,
        ins_index: 0,
    };
    runtime1.run().expect_err("Program did actually finish");

    println!("Part 1: {}", runtime1.accumulator);

    let instructions_count = instructions.len();
    for idx in 0..instructions_count {
        if instructions[idx].instruction_type == InsType::Acc {
            continue;
        }

        let mutated_instructions = instructions
            .iter()
            .enumerate()
            .map(|(idx2, ins)| {
                if idx2 == idx {
                    ins.flipped_jmp_nop()
                } else {
                    ins.clone()
                }
            })
            .collect();

        let mut runtime2 = Runtime {
            instructions: &mutated_instructions,
            accumulator: 0,
            ins_index: 0,
        };
        let result = runtime2.run();

        if result.is_ok() {
            println!("Part 2: {}", runtime2.accumulator);
            break;
        }
    }
}
