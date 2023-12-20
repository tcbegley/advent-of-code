import math
import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field


class Module:
    pass


@dataclass
class FlipFlopModule(Module):
    on: bool = False


@dataclass
class ConjunctionModule(Module):
    memory: dict[str, int] = field(default_factory=dict)


@dataclass
class Network:
    modules: dict[str, Module] = field(default_factory=dict)
    incoming: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    destinations: dict[str, list[str]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def add_module(self, module, destinations):
        if module == "broadcaster":
            self.modules[module] = Module()
        else:
            type_, module = module[0], module[1:]
            self.modules[module] = (
                FlipFlopModule() if type_ == "%" else ConjunctionModule()
            )

        self.destinations[module].extend(destinations)
        for dest in destinations:
            self.incoming[dest].add(module)


def process_row(row):
    source, destinations = row.split(" -> ")
    destinations = destinations.split(", ")
    return source, destinations


def load_data(path):
    with open(path) as f:
        modules = [process_row(row) for row in f.read().strip().split("\n")]

    network = Network()
    for source, destinations in modules:
        network.add_module(source, destinations)

    return network


def process_pulses(pulses, network, modules=None):
    low_pulse_count = high_pulse_count = 0
    low_pulses = []

    while pulses:
        source, module_name, pulse = pulses.popleft()
        if pulse == 1:
            high_pulse_count += 1
        else:
            low_pulse_count += 1

        if modules is not None and pulse == 0 and module_name in modules:
            low_pulses.append(module_name)

        module = network.modules.get(module_name)
        if isinstance(module, FlipFlopModule):
            if pulse == 0:
                module.on = not module.on
                pulse = 1 if module.on else 0
                for destination in network.destinations[module_name]:
                    pulses.append((module_name, destination, pulse))
        elif isinstance(module, ConjunctionModule):
            module.memory[source] = pulse
            pulse = (
                0
                if all(
                    module.memory.get(s, 0) == 1 for s in network.incoming[module_name]
                )
                else 1
            )
            for destination in network.destinations[module_name]:
                pulses.append((module_name, destination, pulse))
        elif isinstance(module, Module):
            # broadcaster module
            for destination in network.destinations[module_name]:
                pulses.append((module_name, destination, pulse))

    if modules is not None:
        return low_pulse_count, high_pulse_count, low_pulses
    return low_pulse_count, high_pulse_count


def part_1(network):
    low_pulse_count = 0
    high_pulse_count = 0

    for _ in range(1_000):
        pulses = deque([(None, "broadcaster", 0)])
        low_inc, high_inc = process_pulses(pulses, network)
        low_pulse_count += low_inc
        high_pulse_count += high_inc

    return low_pulse_count * high_pulse_count


def part_2(network):
    button_presses = 0

    rx_source = next(iter(network.incoming["rx"]))
    modules = list(network.incoming[rx_source])

    cycle_length = {}
    while True:
        button_presses += 1
        _, _, low_pulses = process_pulses(
            deque([(None, "broadcaster", 0)]), network, modules=modules
        )
        for m in low_pulses:
            cycle_length[m] = button_presses

        if len(cycle_length) == 4:
            break

    return math.lcm(*cycle_length.values())


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    data = load_data(sys.argv[1])
    print(f"Part 2: {part_2(data)}")
