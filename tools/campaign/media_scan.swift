// Finds faces and reads text in a list of images, so a person knows where to look.
// It cannot tell a child from an adult and it misses faces. It does not replace looking.
// Build: swiftc -O media_scan.swift -o media_scan
// Run:   ./media_scan list-of-image-paths.txt results.jsonl
import Foundation
import Vision
import ImageIO
// usage: vision <listfile> <out.jsonl>
let args = CommandLine.arguments
let list = try! String(contentsOfFile: args[1]).split(separator: "\n").map(String.init)
FileManager.default.createFile(atPath: args[2], contents: nil)
let out = FileHandle(forWritingAtPath: args[2])!
for p in list {
  autoreleasepool {
    let url = URL(fileURLWithPath: p) as CFURL
    guard let src = CGImageSourceCreateWithURL(url, nil),
          let img = CGImageSourceCreateImageAtIndex(src, 0, [kCGImageSourceShouldAllowFloat: false] as CFDictionary) else { return }
    let w = CGFloat(img.width), h = CGFloat(img.height)
    let props = CGImageSourceCopyPropertiesAtIndex(src, 0, nil) as? [String: Any]
    let orient = (props?["Orientation"] as? UInt32) ?? 1
    let o = CGImagePropertyOrientation(rawValue: orient) ?? .up
    let f = VNDetectFaceRectanglesRequest()
    let t = VNRecognizeTextRequest(); t.recognitionLevel = .accurate; t.usesLanguageCorrection = false
    let hnd = VNImageRequestHandler(cgImage: img, orientation: o, options: [:])
    try? hnd.perform([f, t])
    let faces = (f.results ?? []).map { [$0.boundingBox.origin.x, $0.boundingBox.origin.y, $0.boundingBox.width, $0.boundingBox.height].map { Double(round($0*1000)/1000) } }
    let text = (t.results ?? []).compactMap { $0.topCandidates(1).first?.string }
    let rec: [String: Any] = ["path": p, "w": Int(w), "h": Int(h), "faces": faces, "text": text]
    if let d = try? JSONSerialization.data(withJSONObject: rec) { out.write(d); out.write("\n".data(using: .utf8)!) }
  }
}
