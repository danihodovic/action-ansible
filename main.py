import os
import shutil
import tempfile

import ansible_runner


def parse_env():
    ansible_env = {}
    for key, value in os.environ.items():
        if key.startswith("ANSIBLE_"):
            ansible_env[key] = value
    return ansible_env



def main():
    playbook = os.getenv("PLAYBOOK")
    original_playbook_dir = os.getenv("PLAYBOOK_DIR")
    with tempfile.TemporaryDirectory(prefix="ansibl-") as tmp_dir:
        playbook_dir = os.path.join(tmp_dir, "playbooks")
        shutil.copytree(
            original_playbook_dir,
            playbook_dir,
            ignore=shutil.ignore_patterns("*.pyc", ".git", ".venv"),
        )
        ansible_env = parse_env()

        vault_password = os.getenv("VAULT_PASSWORD")
        if vault_password:
            with tempfile.NamedTemporaryFile("w", delete=False) as vault_file:
                vault_file.write(vault_password)
                ansible_env["ANSIBLE_VAULT_PASSWORD_FILE"] = vault_file.name

        ansible_runner.run(
            playbook=playbook, private_data_dir=playbook_dir, envvars=ansible_env
        )


if __name__ == "__main__":
    main()
