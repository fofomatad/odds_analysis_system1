{
  description = "Python environment for odds analysis system";
  deps = [
    python39Full
    python39Packages.pip
    python39Packages.flask
    python39Packages.pandas
    python39Packages.numpy
    python39Packages.requests
  ];
} 