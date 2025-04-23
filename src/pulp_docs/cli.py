import click

from mkdocs.__main__ import cli as mkdocs_cli
from pulp_docs.context import (
    ctx_blog,
    ctx_docstrings,
    ctx_draft,
    find_paths,
    RepoFindSpec,
)
from pathlib import Path


def blog_callback(ctx: click.Context, param: click.Parameter, value: bool) -> bool:
    ctx_blog.set(value)
    return value


def docstrings_callback(
    ctx: click.Context, param: click.Parameter, value: bool
) -> bool:
    ctx_docstrings.set(value)
    return value


def draft_callback(ctx: click.Context, param: click.Parameter, value: bool) -> bool:
    ctx_draft.set(value)
    return value


def find_paths_callback(
    ctx: click.Context, param: click.Parameter, value: bool
) -> bool:
    result = [item.strip() for item in value.split(";") if item.strip()]
    find_paths.set(result)
    return result


blog_option = click.option(
    "--blog/--no-blog",
    default=True,
    expose_value=False,
    callback=blog_callback,
    help="Build blog.",
)

docstrings_option = click.option(
    "--docstrings/--no-docstrings",
    default=True,
    expose_value=False,
    callback=docstrings_callback,
    help="Enable mkdocstrings plugin.",
)

draft_option = click.option(
    "--draft/--no-draft",
    expose_value=False,
    callback=draft_callback,
    help="Don't fail if repositories are missing.",
)

paths_option = click.option(
    "--paths",
    envvar="PULPDOCS_PATHS",
    expose_value=False,
    default="",
    callback=find_paths_callback,
    help="A semicolon separated list of repository paths. Accept glob patterns.",
)


main = mkdocs_cli

for command_name in ["build", "serve"]:
    sub_command = main.commands.get(command_name)
    draft_option(sub_command)
    blog_option(sub_command)
    docstrings_option(sub_command)
    paths_option(sub_command)
    serve_options = sub_command.params
    config_file_opt = next(filter(lambda opt: opt.name == "config_file", serve_options))
    config_file_opt.envvar = "PULPDOCS_DIR"
