import java.io.*;
 
import com.snowtide.pdf.PDFTextStream;
import com.snowtide.pdf.OutputTarget;

public class TextStream {

    public static void main (String[] args) throws IOException {
        File pdfFile = new File(args[0]);
        File textFile = new File(args[1]);

        PDFTextStream stream = new PDFTextStream(pdfFile); 
        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(textFile))); 
        OutputTarget tgt = new OutputTarget(writer); 
        stream.pipe(tgt); 
     
        writer.flush(); 
        writer.close(); 
        stream.close(); 
    }
}
