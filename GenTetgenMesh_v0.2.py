# Python Script, API Version = V16
import os, sys,time
from os import path
import subprocess
import shutil

######## User Input ##########
# please provide the path to tetgen.exe, 
PathToTetgen143 = "D:\Program\\tetgen1.4.3-build\Release\\tetgen.exe" 
PathToTetgen150 = "D:\Program\\tetgen-1.5.0-build\Release\\tetgen.exe" 
#OutputDir = "D:\VirtualMachine\share\ITER_upperport" 
OutputDir = "D:\WorkingDir\IFMIF_DONES\\28_HFTM_mesh\\2_meshes" 
# whether rename all the selected solids: True/False
RenameSolids = True 
# whether renew all the folders: True/False
RenewFolders = True
##############################

#initial the output folders
StepFolder=OutputDir + "\\StepFiles"
TempFolder=OutputDir + "\\TempFiles"
MeshFolder=OutputDir + "\\MeshFiles"
if RenewFolders:
    if os.path.exists(StepFolder):
        shutil.rmtree(StepFolder)
    os.makedirs(StepFolder) 
    if os.path.exists(TempFolder):
        shutil.rmtree(TempFolder)
    os.makedirs(TempFolder)
    if os.path.exists(MeshFolder):
        shutil.rmtree(MeshFolder) 
    os.makedirs(MeshFolder)

# obtain all solids in the root
SolidList = GetRootPart().Bodies
if Selection.GetActive().Items.Count != 0 :
    SolidList = Selection.GetActive().Items
#counters
i=0
iFailed=0
for iBody in SolidList : 
    i=i+1
    iBodyName = iBody.Name
    if RenameSolids :
        iBodyName = "part-"+ str(i)
    iBody.Name = iBodyName
    sel = Selection.Create(iBody)
    result = Copy.ToClipboard(sel)
    #create a new document to save the solid to STEP and STL file
    DocumentHelper.CreateNewDocument() 
    result = Paste.FromClipboard()
    StepFileName=StepFolder + "\\"+iBodyName+".step"
    DocumentSave.Execute(StepFileName,ExportOptions.Create() )
    STLFileName=TempFolder + "\\"+iBodyName+".stl"
    expOp = ExportOptions.Create()
    #print expOp.Stl.Tessellation.SurfaceDeviation
    DocumentSave.Execute(STLFileName,expOp )
    # deletSelection.Create(Mesh1)e the solid in this document
    Delete.Execute(Selection.SelectAll())
    time.sleep(0.5)
    #run tetgen 1.4.3 first
    retn = subprocess.call([PathToTetgen150, ' -p ', STLFileName])
    #print retn
    time.sleep(0.5)
    NodeFileName=TempFolder + "\\"+iBodyName+".1.node"
    ElementFileName=TempFolder + "\\"+iBodyName+".1.ele"
    AbaqusFileName=MeshFolder + "\\"+iBodyName+".inp"
    #if not OK, use tetgen 1.5.0 to try again
    Success = ( retn == 0 and  os.path.isfile(NodeFileName)  and os.path.isfile(ElementFileName) )
    if not Success :
        retn = subprocess.call([PathToTetgen143, ' -p ', STLFileName])
    # if not OK, import the STL file and indicate the error solid
    Success = ( retn == 0 and  os.path.isfile(NodeFileName)  and os.path.isfile(ElementFileName) )
    if not Success :
        iFailed = iFailed +1
        print "ERROR: ", iBodyName, " meshing failed..."
        DocumentInsert.Execute(STLFileName,FileSettings1 )
        #copy the error faceted solids to the working document
        sel2 = Selection.Create(GetRootPart().Components[0])
        #selall.Items[0].Name= iBody.Name + "-err"
        #Copy.ToClipboard(Selection.SelectAll())
        Copy.ToClipboard(sel2)
        CloseWindow() 
        # delete the original solid
        result = Paste.FromClipboard()
        iBody.Name = iBody.Name + "-err"
    # if OK, read the mesh and convert it into abaqus format
    else : 
        CloseWindow()
        NodeFile = open(NodeFileName, 'r')
        ElmFile = open(ElementFileName, 'r')
        OutFile = open(AbaqusFileName, 'w')

        # check the node file
        NodeInfoLine = NodeFile.readline()
        aSplit= NodeInfoLine.split()
        if len(aSplit) != 4 or int(aSplit[1]) != 3:
            print "node file info error of ",iBodyName, "!"
            quit()
        NodeTotal = int(aSplit[0])

        # check the element file
        ElmInfoLine = ElmFile.readline()
        aSplit= ElmInfoLine.split()
        if len(aSplit) != 3 or int(aSplit[1]) != 4:
            print "elment file info error, or unsupported element type! ", iBodyName
            quit()
        ElmTotal = int(aSplit[0])

        # print the header of abaqus file
        PartName = iBodyName
        OutFile.write("*Heading\n** Created by SpaceClaim tetgen meshing script\n** further infomation contact yuefeng.qiu@kit.edu\n*Preprint, echo=NO, model=NO, history=NO, contact=NO\n")
        OutFile.write("*Part, name=Part-" + PartName + "\n")
        OutFile.write("*Node\n")

        #print the nodes
        for idx in range(NodeTotal) :
            aLine = NodeFile.readline()
            aSplit = aLine.split()
            if len(aSplit) != 4 or int(aSplit[0]) != idx+1:
                print "error in parsing line ", idx + 2 , " of the node file."; sys.exit()
                #quit()
            OutFile.write(aSplit[0] + ", " + aSplit[1] + ", " + aSplit[2] + ", " + aSplit[3] + "\n")

        #print the elements
        OutFile.write("*Element, type=C3D4\n")
        for idx in range(ElmTotal) :
            aLine = ElmFile.readline()
            aSplit = aLine.split()
            if len(aSplit) != 5 or int(aSplit[0]) != idx+1:
                print "error in parsing line ", idx + 2 , " of the element file."; sys.exit()
            OutFile.write(aSplit[0] + ", " + aSplit[1] + ", " + aSplit[2] + ", " + aSplit[3] + ", " + aSplit[4] +"\n")

        #print ending of this part
        OutFile.write("*Nset, nset=Set-material_" + PartName + "_1, generate\n")	
        OutFile.write("   1,  "+ str(NodeTotal) +",    1\n")
        OutFile.write("*Elset, elset=Set-material_" + PartName + "_1, generate\n")	
        OutFile.write("   1,  "+ str( ElmTotal) +",    1\n")
        OutFile.write("*Nset, nset=Set-statistic_" + PartName + "_1, generate\n")	
        OutFile.write("   1,  "+ str( NodeTotal) +",    1\n")
        OutFile.write("*Elset, elset=Set-statistic_" + PartName + "_1, generate\n")	
        OutFile.write("   1,  "+str( ElmTotal) +",    1\n")
        OutFile.write("*End Part\n")
        #print ending of the abaqus file
        OutFile.write("*Assembly, name=Assembly\n")
        OutFile.write("*Instance, name=Part-" + PartName + "-1, part=Part-" + PartName +"\n")
        OutFile.write("*End Instance\n")
        OutFile.write("*End Assembly\n")
        OutFile.write("*Material, name=material_" + PartName + "_1\n")
        NodeFile.close()
        ElmFile.close()
        OutFile.close()
        time.sleep(0.1)
        print iBodyName, "meshing success!"
print "---Total: ", i, " solids,  ", i-iFailed, " success, ", iFailed, " failed.---"


