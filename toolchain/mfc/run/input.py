
import os
import json
import dataclasses

import common

@dataclasses.dataclass
class MFCInputFile:
    filename:     str
    case_dirpath: str
    case_dict:    dict

    # Generate case.fpp
    def create(self, target_name: str) -> None:
        # === case.fpp ===
        filepath = f"{os.getcwd()}/src/common/case.fpp"
        content  = f"""\
! This file was generated by MFC to
! describe the case one wishes to run.

#:set CASE={self.case_dict}
#:set CODE="{target_name}"

"""

        # Check if this case already has a case.fpp file.
        # If so, we don't need to generate a new one, which
        # would cause a partial and unnecessary rebuild.
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                if f.read() == content:
                    return

        common.file_write(filepath, content)


# Load the input file
def load(filename: str) -> MFCInputFile:
    dirpath:    str  = os.path.abspath(os.path.dirname(filename))
    dictionary: dict = {}

    if not os.path.exists(filename):
        raise common.MFCException(f"Input file '{filename}' does not exist. Please check the path is valid.")

    if filename.endswith(".py"):
        (json_str, err) = common.get_py_program_output(filename)

        if err != 0:
            raise common.MFCException(f"Input file {filename} terminated with a non-zero exit code. Please make sure running the file doesn't produce any errors.")
    elif filename.endswith(".json"):
        json_str = common.file_read(filename)
    else:
        raise common.MFCException("Unrecognized input file format. Only .py and .json files are supported. Please check the README and sample cases in the samples directory.")
    
    try:
        dictionary = json.loads(json_str)
    except Exception as exc:
        raise common.MFCException(f"Input file {filename} did not produce valid JSON. It should only print the case dictionary.\n\n{exc}\n")

    return MFCInputFile(filename, dirpath, dictionary)
