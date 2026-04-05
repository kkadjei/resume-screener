import click
from screener import screen_resumes, save_results


@click.command()
@click.option("--job", "-j", required=True, help="Path to a .txt file containing the job description.")
@click.option("--resumes", "-r", required=True, help="Path to the folder containing PDF resumes.")
@click.option("--output", "-o", default=None, help="Optional path to save results as JSON.")
@click.option("--top", "-t", default=None, type=int, help="Show only the top N results.")
def main(job, resumes, output, top):
    """ AI-Powered Resume Screener — ranks resumes by relevance to a job description."""

    if job.endswith(".txt"):
        with open(job, "r") as f:
            job_description = f.read().strip()
    else:
        job_description = job

    click.echo(f"\n Scanning resumes in: {resumes}\n")

    results = screen_resumes(job_description, resumes)

    if not results:
        click.echo(" No PDF resumes found in the specified directory.")
        return

    if top:
        results = results[:top]

    click.echo(f"{'Rank':<6} {'Score':<10} {'Filename'}")
    click.echo("-" * 50)
    for i, r in enumerate(results, 1):
        bar = "█" * int(r["score"] / 5)
        click.echo(f"{i:<6} {r['score']:<10} {r['filename']}")
        click.echo(f"       {bar} {r['score']}%")
        click.echo(f"       Preview: {r['preview'][:120]}...\n")

    if output:
        save_results(results, output)
        click.echo(f"\n Results saved to {output}")


if __name__ == "__main__":
    main()