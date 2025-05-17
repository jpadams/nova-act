import dagger
from dagger import dag, function, object_type


@object_type
class NovaAct:
    @function
    def search(self, starting_page: str, assignment: str, api_key: dagger.Secret) -> dagger.Container:
        """Container with nova-act enviro which has recorded session results"""
        return (
            dag
            .container()
            .from_("python:3.12-slim")
            .with_workdir("/app")
            .with_directory("/app/nova-act-logs", dag.directory())
            .with_exec(["pip", "install", "nova-act"])
            .with_secret_variable("NOVA_ACT_API_KEY", api_key)
            .with_env_variable("NOVA_ACT_HEADLESS", "1")
            .with_new_file(
                "search.py",
                f"""
from nova_act import NovaAct

with NovaAct(starting_page="{starting_page}", logs_directory="/app/nova-act-logs", record_video=True) as nova:
    nova.act("{assignment}")
"""
            )
            .with_exec(["python", "search.py"])
        )
