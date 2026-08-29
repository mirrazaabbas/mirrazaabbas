import json
from pathlib import Path

PROMPTS_FILE = Path(__file__).with_name("prompts.json")


def load_prompts() -> list[dict]:
    with PROMPTS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_prompt(template: dict, values: dict[str, str]) -> str:
    prompt = template["template"]
    for key, value in values.items():
        prompt = prompt.replace("{" + key + "}", value.strip())
    return prompt


def choose_template(prompts: list[dict]) -> dict:
    print("\nPrompt Engineering Lab\n")
    for index, prompt in enumerate(prompts, start=1):
        print(f"{index}. {prompt['name']} — {prompt['description']}")

    while True:
        try:
            choice = int(input("\nChoose a template: "))
            if 1 <= choice <= len(prompts):
                return prompts[choice - 1]
        except ValueError:
            pass
        print("Please enter a valid number.")


def main() -> None:
    prompts = load_prompts()
    selected = choose_template(prompts)

    values = {}
    for variable in selected["variables"]:
        values[variable] = input(f"{variable.replace('_', ' ').title()}: ")

    final_prompt = build_prompt(selected, values)
    print("\n--- Generated Prompt ---\n")
    print(final_prompt)


if __name__ == "__main__":
    main()
