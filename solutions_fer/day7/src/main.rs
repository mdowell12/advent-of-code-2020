use std::collections::{HashMap, HashSet};
use std::io::{self, BufRead};
extern crate regex;
use regex::Regex;

struct Graph {
    edge_map: HashMap<String, Vec<WeightedEdge>>,
}

#[derive(Clone)]
struct WeightedEdge {
    weight: usize,
    node: String,
}

impl Graph {
    pub fn new() -> Self {
        Self {
            edge_map: HashMap::new(),
        }
    }

    pub fn add_edge(&mut self, node1: String, node2: WeightedEdge) {
        self.edge_map.entry(node1).or_insert(vec![]).push(node2);
    }

    pub fn get(&self, node: &str) -> Option<&Vec<WeightedEdge>> {
        self.edge_map.get(node)
    }

    pub fn unique_bags_in(&self, node: &str) -> HashSet<String> {
        self.get(node)
            .and_then(|node| {
                Some(
                    node.iter()
                        .map(|edge| {
                            let mut set = HashSet::new();
                            set.insert(edge.node.clone());
                            set.extend(self.unique_bags_in(&edge.node));
                            set
                        })
                        .fold(HashSet::new(), |mut memo, count| {
                            memo.extend(count);
                            memo
                        }),
                )
            })
            .unwrap_or(HashSet::new())
    }

    pub fn weighted_bags_in(&self, node: &WeightedEdge) -> usize {
        self.get(&node.node)
            .and_then(|edges| {
                Some(
                    edges
                        .iter()
                        .map(|edge| self.weighted_bags_in(&edge) * edge.weight)
                        .sum::<usize>()
                        + 1,
                )
            })
            .unwrap_or(1)
    }
}

fn main() {
    let (contains_bag_graph, contained_bag_graph) = build_graph();
    println!(
        "Part 1: {}",
        contains_bag_graph.unique_bags_in("shiny gold").len()
    );
    println!(
        "Part 2: {}",
        contained_bag_graph.weighted_bags_in(&WeightedEdge {
            weight: 1,
            node: String::from("shiny gold")
        }) - 1
    );
}

fn build_graph() -> (Graph, Graph) {
    let stdin = io::stdin();
    let mut contains_bag_graph = Graph::new();
    let mut contained_bag_graph = Graph::new();

    let contains_re =
        Regex::new(r"^(?P<container>[a-z ]+) bags contain (?P<contained>.+)\.$").unwrap();
    let contained_re =
        Regex::new(r"(?P<contained_number>\d+) (?P<contained_name>[a-z ]+) bag").unwrap();

    for elem in stdin.lock().lines() {
        let line = elem.unwrap();

        if let Some(caps) = contains_re.captures(&line) {
            let container = caps.name("container").unwrap().as_str();

            let contained = caps.name("contained").unwrap().as_str();
            for cap2 in contained_re.captures_iter(contained) {
                let contained_name = cap2.name("contained_name").unwrap().as_str();
                let contained_number = cap2
                    .name("contained_number")
                    .unwrap()
                    .as_str()
                    .parse::<usize>()
                    .unwrap();

                let weighted_edge1 = WeightedEdge {
                    weight: contained_number,
                    node: container.to_string(),
                };
                contains_bag_graph.add_edge(contained_name.to_string(), weighted_edge1);

                let weighted_edge2 = WeightedEdge {
                    weight: contained_number,
                    node: contained_name.to_string(),
                };
                contained_bag_graph.add_edge(container.to_string(), weighted_edge2);
            }
        }
    }

    (contains_bag_graph, contained_bag_graph)
}
