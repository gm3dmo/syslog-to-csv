
if __name__ == "__main__":

    dist = distribution("bundlefun")

    data_path = dist.locate_file("log-formats.json")

    print(type(data_path), data_path)

    exit(main())

