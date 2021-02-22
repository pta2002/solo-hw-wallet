let pkgs = import <nixpkgs> {};
in
pkgs.mkShell {
    buildInputs = with pkgs; [
        python3
        python3Packages.solo-python
        libsodium
        gcc-arm-embedded
    ];
    name = "solo";
}
