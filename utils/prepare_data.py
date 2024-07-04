import argparse
import os
import glob
import random
import logging

logging.basicConfig(format="%(message)s")


def list_files(directory):
    """Helper function to list files in a directory for debugging."""
    if os.path.exists(directory):
        print(f"Directory exists: {directory}")
        print(f"Files: {os.listdir(directory)}")
    else:
        print(f"Directory does not exist: {directory}")


def prepare_pretraining_data(src1, src2, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    src1_all_lines = []
    src2_all_lines = []

    list_files(src1)
    src1_paths = sorted(glob.glob(os.path.join(src1, "*")))
    if src2:
        list_files(src2)
        src2_paths = sorted(glob.glob(os.path.join(src2, "*")))
    else:
        src2_paths = src1_paths

    print(f"src1_paths: {src1_paths}")
    print(f"src2_paths: {src2_paths}")

    assert len(src1_paths) == len(src2_paths)

    for src1_file, src2_file in zip(src1_paths, src2_paths):
        assert src1_file.split("/")[-1] == src2_file.split("/")[-1]

        src1_lines = open(src1_file, encoding="utf8").readlines()
        src2_lines = open(src2_file, encoding="utf8").readlines()

        if len(src1_lines) != len(src2_lines):
            logging.warning(
                "WARNING: Unequal lines in: {} {}".format(src1_file, src2_file)
            )
            continue

        for src1_line, src2_line in zip(src1_lines, src2_lines):
            if (not src1_line.strip()) or (not src2_line.strip()):
                logging.info(
                    "WARNING: Skipping blank lines in: {} {}".format(
                        src1_file, src2_file
                    )
                )
                continue
            src1_all_lines.append(src1_line)
            src2_all_lines.append(src2_line)

    open("{}/pretrain_src1.txt".format(output_folder), "w", encoding="utf8").write(
        "".join(src1_all_lines)
    )
    if src2:
        open("{}/pretrain_src2.txt".format(output_folder), "w", encoding="utf8").write(
            "".join(src2_all_lines)
        )


def write_training_data(filenames, output_name, check):
    src1_all_lines = []
    src2_all_lines = []
    tgt_all_lines = []

    for src1_file, src2_file, tgt_file in filenames:
        assert (
            os.path.basename(src1_file)
            == os.path.basename(src2_file)
            == os.path.basename(tgt_file)
        )

        src1_lines = open(src1_file, encoding="utf8").readlines()
        src2_lines = open(src2_file, encoding="utf8").readlines() if src2_file else []
        tgt_lines = open(tgt_file, encoding="utf8").readlines()

        if len(src1_lines) != len(tgt_lines):
            logging.warning(
                "WARNING: Unequal lines in: {} {}".format(src1_file, tgt_file)
            )
            continue

        for src1_line, tgt_line in zip(src1_lines, tgt_lines):
            if (not src1_line.strip()) or (not tgt_line.strip()):
                logging.info(
                    "WARNING: Skipping blank lines in: {} {}".format(
                        src1_file, tgt_file
                    )
                )
                continue
            src1_all_lines.append(src1_line)
            if src2_lines:
                src2_all_lines.append(src2_lines[src1_lines.index(src1_line)])
            tgt_all_lines.append(tgt_line)

    open("{}src1.txt".format(output_name), "w", encoding="utf8").write(
        "".join(src1_all_lines)
    )
    if check and src2_all_lines:
        open("{}src2.txt".format(output_name), "w", encoding="utf8").write(
            "".join(src2_all_lines)
        )
    open("{}tgt.txt".format(output_name), "w", encoding="utf8").write(
        "".join(tgt_all_lines)
    )


def prepare_training_data(src1, src2, tgt, output_folder, training_frac):
    assert training_frac < 1.0

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    list_files(src1)
    src1_paths = sorted(glob.glob(os.path.join(src1, "*")))
    if src2:
        list_files(src2)
        check = True
        src2_paths = sorted(glob.glob(os.path.join(src2, "*")))
    else:
        check = False
        src2_paths = src1_paths
    list_files(tgt)
    tgt_paths = sorted(glob.glob(os.path.join(tgt, "*")))

    print(f"src1_paths: {src1_paths}")
    print(f"src2_paths: {src2_paths}")
    print(f"tgt_paths: {tgt_paths}")

    assert len(src1_paths) == len(src2_paths) == len(tgt_paths)

    all_files = list(zip(src1_paths, src2_paths, tgt_paths))
    random.shuffle(all_files)

    num_files = len(all_files)
    train_idx = round(training_frac * num_files)
    dev_idx = train_idx + round((1.0 - training_frac) * num_files / 2)

    print(f"Number of files: {num_files}")
    print(f"Train index: {train_idx}, Dev index: {dev_idx}")

    if dev_idx <= train_idx or dev_idx == num_files:
        logging.error(
            "ERROR: Fractions for data split are not usable with the dataset size. Adjust the parameter and try again. "
        )
        return

    write_training_data(all_files[:train_idx], f"{output_folder}/train_", check)
    write_training_data(all_files[train_idx:dev_idx], f"{output_folder}/dev_", check)
    write_training_data(all_files[dev_idx:], f"{output_folder}/test_", check)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--unannotated_src1")
    parser.add_argument("--unannotated_src2")
    parser.add_argument("--annotated_src1")
    parser.add_argument("--annotated_src2")
    parser.add_argument("--annotated_tgt")
    parser.add_argument("--output_folder")
    parser.add_argument("--training_frac", type=float, default=0.8)
    args = parser.parse_args()

    prepare_pretraining_data(
        src1=args.unannotated_src1,
        src2=args.unannotated_src2,
        output_folder=f"{args.output_folder}/pretraining"
    )

    prepare_training_data(
        src1=args.annotated_src1,
        src2=args.annotated_src2,
        tgt=args.annotated_tgt,
        output_folder=f"{args.output_folder}/training",
        training_frac=args.training_frac
    )
