import click
import datacompy
import pandas as pd

from quantms_io.core.feature import FeatureHandler
from quantms_io.core.project import check_directory,get_project_accession,create_uuid_filename
from quantms_io.core.tools import plot_peptidoform_charge_venn, plot_sequence_venn


@click.command(
    "convert-feature-file", short_help="Convert msstats/mztab to parquet file"
)
@click.option(
    "--sdrf_file",
    help="the SDRF file needed to extract some of the metadata",
    required=True,
)
@click.option(
    "--msstats_file",
    help="the MSstats input file, this will be considered the main format to convert",
    required=True,
)
@click.option(
    "--mztab_file",
    help="the mzTab file, this will be used to extract the protein information",
    required=True,
)
@click.option(
    "--consensusxml_file",
    help="the consensusXML file used to retrieve the mz/rt",
    required=False,
)
@click.option(
    "--use_cache",
    help="Use cache instead of in memory conversion",
    required=False,
    is_flag=True,
)
@click.option(
    "--generate_project",
    help="Generate project.json for pride project, Otherwise, False",
    required=False,
    is_flag=True,
)
@click.option(
    "--output_folder",
    help="Folder where the Json file will be generated",
    required=True,
)
@click.option("--output_prefix_file", help="Prefix of the Json file needed to generate the file name", required=False)
def convert_feature_file(
    sdrf_file: str,
    msstats_file: str,
    mztab_file: str,
    consensusxml_file: str,
    use_cache: bool,
    generate_project: bool,
    output_folder: str,
    output_prefix_file: str,
):
    """
    Convert a msstats/mztab file to a parquet file. The parquet file will contain the features and the metadata.
    :param sdrf_file: the SDRF file needed to extract some of the metadata
    :param msstats_file: the MSstats input file, this will be considered the main format to convert
    :param mztab_file: the mzTab file, this will be used to extract the protein information
    :param consensusxml_file: the consensusXML file used to retrieve the mz/rt
    :param use_cache: Use cache instead of in memory conversion
    :param generate_project: "Generate project.json for pride project, Otherwise, False"
    :param output_folder: Folder where the Json file will be generated
    :param output_prefix_file: Prefix of the Json file needed to generate the file name
    :return: none
    """

    if (
        sdrf_file is None
        or msstats_file is None
        or mztab_file is None
        or output_folder is None
    ):
        raise click.UsageError("Please provide all the required parameters")
    
    if generate_project:
        Project = check_directory(output_folder)
        project_accession = Project.project.project_info["project_accession"]

    if use_cache is None:
        use_cache = False

    feature_manager = FeatureHandler()
    if not output_prefix_file:
        if generate_project:
            output_prefix_file = project_accession
        else:
            output_prefix_file = ''
    feature_manager.parquet_path = output_folder + "/" + create_uuid_filename(output_prefix_file,'.featrue.parquet')
    if consensusxml_file is not None:
        feature_manager.convert_mztab_msstats_to_feature(
            mztab_file=mztab_file,
            msstats_file=msstats_file,
            sdrf_file=sdrf_file,
            output_folder = output_folder,
            consesusxml_file=consensusxml_file,
            use_cache=use_cache,
            generate_project = generate_project
        )
    else:
        feature_manager.convert_mztab_msstats_to_feature(
            mztab_file=mztab_file,
            msstats_file=msstats_file,
            sdrf_file=sdrf_file,
            output_folder = output_folder,
            use_cache=use_cache,
            generate_project = generate_project
        )
