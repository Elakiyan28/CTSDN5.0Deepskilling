
// Task 1: Create Database & Collection


use college_nosql;

db.createCollection("feedback");

// Insert sample documents (at least 10, varied ratings/tags/semesters)
db.feedback.insertMany([
    {
        student_id: 1,
        course_code: "CS101",
        semester: "2022-ODD",
        rating: 4,
        comments: "Excellent teaching. Would recommend.",
        tags: ["challenging", "well-structured", "good-examples"],
        submitted_at: ISODate("2022-11-30T10:15:00Z"),
        attachments: [{ filename: "notes.pdf", size_kb: 240 }]
    },
    {
        student_id: 2,
        course_code: "CS102",
        semester: "2022-ODD",
        rating: 5,
        comments: "Great examples and clarity.",
        tags: ["clear", "engaging"],
        submitted_at: ISODate("2022-11-30T11:00:00Z")
    },
    {
        student_id: 3,
        course_code: "CS101",
        semester: "2022-ODD",
        rating: 2,
        comments: "Needs improvement.",
        tags: ["confusing"],
        submitted_at: ISODate("2022-12-01T09:30:00Z")
    }

]);


db.feedback.countDocuments();


// Task 2: CRUD Operations


// READ: Find all feedback with rating = 5
db.feedback.find({ rating: 5 });

// READ: Feedback for CS101 with tag 'challenging'
db.feedback.find({ course_code: "CS101", tags: "challenging" });

// READ: Projection (only student_id, course_code, rating)
db.feedback.find({}, { student_id: 1, course_code: 1, rating: 1, _id: 0 });

// UPDATE: Mark low ratings (<3) as needs_review
db.feedback.updateMany(
    { rating: { $lt: 3 } },
    { $set: { needs_review: true } }
);

// UPDATE: Push new tag 'reviewed' where needs_review = true
db.feedback.updateMany(
    { needs_review: true },
    { $push: { tags: "reviewed" } }
);

// DELETE: Remove feedback from semester '2021-EVEN'
db.feedback.deleteMany({ semester: "2021-EVEN" });



// Task 3: Aggregation Pipelines


//  Avg rating per course for semester '2022-ODD'
db.feedback.aggregate([
    { $match: { semester: "2022-ODD" } },
    { $group: { _id: "$course_code", avg_rating: { $avg: "$rating" }, total_feedback: { $sum: 1 } } },
    { $sort: { avg_rating: -1 } },
    { $project: { course_code: "$_id", average_rating: { $round: ["$avg_rating", 1] }, total_feedback: 1, _id: 0 } }
]);

//  Count tag frequency
db.feedback.aggregate([
    { $unwind: "$tags" },
    { $group: { _id: "$tags", count: { $sum: 1 } } },
    { $sort: { count: -1 } }
]);
