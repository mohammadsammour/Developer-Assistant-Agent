from src.agent import run_agent


def main():
    print("Developer Assistant")
    print("-" * 30)

    user_request = input("What do you want help with?\n> ")

    code_context = input("\nPaste code/context if you have any. Press Enter to skip:\n> ")

    report = run_agent(
        user_request=user_request,
        code_context=code_context,
    )

    print("\n--- Developer Task Report ---")
    print(f"Task type: {report.task_type}")
    print(f"Difficulty: {report.difficulty}")
    print(f"Risk level: {report.risk_level}")
    print(f"Summary: {report.summary}")

    print("\nKey points:")
    for point in report.key_points:
        print(f"- {point}")

    print("\nPotential bugs:")
    if report.potential_bugs:
        for bug in report.potential_bugs:
            print(f"- {bug.bug}: {bug.explanation}")
    else:
        print("- No potential bugs found.")

    print("\nNext steps:")
    for step in report.next_steps:
        print(f"- {step}")

    print(f"\nNeeds human review: {report.needs_human_review}")


if __name__ == "__main__":
    main()