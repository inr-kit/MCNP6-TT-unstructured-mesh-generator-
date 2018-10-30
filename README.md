# MCNP6 unstructured mesh generator using TT approach



MCNP6 unstructured mesh generator using the tessellation-tetrahedralization approach.
The tesselalation-tetrahedralization approach uses CAD software to produce first the facets,
and then uses tetgen code to produce tetrahdral mesh keeping the facets as surface mesh. In this way
the number of mesh elements can be largely reduced at the same time keeping high geometry accuracy.
This type of mesh is very useful for unstructured mesh modeling of MCNP6. 

This package contains three main items

 
  * GenTetgenMesh_v0.2.scscript: a SpaceClaim python script which run the job of mesh generation in SpaceClaim
  * tetgen-1.5.0-build and tetgen1.4.3-build: tetgen executable in two versions
  * README.md: this file

********Installation and useage********  
To use this package, you need SpaceClaim version 2016 (R 17.1) or later.

* Download the package in to a folder, here brief as $TTMESH. 
   * Please noted that the folder name of any upper level folder should NOT start with character "t" and "n" due to python linguistics. 
   
   * For example, folder "D:\tomorrow\now" is a bad folder to place this package. 

* Start SpaceClaim, and load the example CAD model for mesh generation.

* Load the conversion script. 
   * click File->Open, change folder to $TTMESH 
   
   * select the file type "SpaceClaim Script (*.scscript, *.py)" at the right-below corner    
   
   * select the  script "GenTetgenMesh_v0.2.scscript". 
   * the script will be display along side with the CAD model.

* Using the script to generated the mesh.
   * For the fisrt time, you have to provide the path of the tetgen.exe to the script. In the very begin of the script "User Input" provide the full path of "$MCCAD\tetgen1.4.3-build" to the variable "PathToTetgen143", and the  full path of "$MCCAD\tetgen-1.5.0-build" to the variable "PathToTetgen150".
   * Specified the "OutputDir" folder to output the meshes and intermediate files. 
   * Copy the solid in to a  new SpaceClaim design, make sure that the solids are NOT located in any components.
   * Click the green Play button to run the script. 
 * Generated the MCNP unstructured mesh model
   * McCad-SALOME program is needed for generated the model, please find the code [here](https://github.com/inr-kit/McCad-Salome-Binaries).
   * Import first the CAD solid in the $OutputDir/Stepfiles into McCad program.
   * Import the Abaqus meshes in the $OutputDir/MeshFiles into McCad program also. They will be imported into the SALOME-SMESH module. Right click those meshes and use "Import SMESH objects", and assigned to the consistent CAD solids at the same time. Please keep the consistent and matching the solid and mesh one-by-one to avoid mistakes. 
   * Further instructions please read the McCad manual.

********General Suggestion********    

* This tool is in preliminary stage, please tolerate the error and crashes. 

* If you have any questions please contact the developer directly for assistance. 

********!!! SpaceClaim Crash !!!********  
* Sometimes SpaceClaim graphic will crash due to too fast graphical refreshing. If you encounter this problem, here is some way to mitigate the problem:
   
   * At File->SpaceClaim Options->Advanced, UNCHECK the option "Animate Changes to the view projection".
   
   * Minimize the SpaceClaim window during the script running. 
   

for further information or question please contact yuefeng.qiu@kit.edu. 
