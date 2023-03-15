{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = with pkgs; [
    python312
    glib
    pango
    cairo
    gdk-pixbuf
    libffi
    fontconfig
    freetype
    harfbuzz
    libpng
    libjpeg
    pixman
  ];

  shellHook = ''
    export LD_LIBRARY_PATH=${pkgs.glib.out}/lib:${pkgs.pango.out}/lib:${pkgs.cairo.out}/lib:${pkgs.gdk-pixbuf.out}/lib:${pkgs.libffi.out}/lib:${pkgs.fontconfig.lib}/lib:${pkgs.freetype.out}/lib:${pkgs.harfbuzz.out}/lib:${pkgs.pixman.out}/lib:${pkgs.libpng.out}/lib:${pkgs.libjpeg.out}/lib:$LD_LIBRARY_PATH
  '';
}
