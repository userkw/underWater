UnderWater

UnderWater helps make underwater photos clearer and more colorful. Users can upload photos, enhance them with filters, and see the original and enhanced photos side-by-side.


Introduction

UnderWater assists marine biologists, underwater photographers, and researchers by enhancing underwater images.

Deployed Project: https://www.youtube.com/watch?v=6QXPURvZmSg
LinkedIn: https://www.linkedin.com/in/kawthar-e-1889b9318/  
Final Project Blog Article: https://medium.com/@user.kw/project-blog-underwater-filters-2756997afc7e

Installation

1. Clone the repository:
    git clone https://github.com/userkw/underwater.git

2. Navigate to the project directory:
    cd underwater

3. Install the dependencies:
    pip install -r requirements.txt
    cd frontend
    npm install

Usage

1. Start the Flask backend:
    python app.py

2. Start the Next.js frontend:
    npm run dev

3. Open http://localhost:3000 in your browser.

Key Features

- Upload and enhance underwater photos.
- Download improved photos.
- Side-by-side comparison of original and enhanced photos.

Technologies Used

- Frontend: Next.js
- Backend: Python, Flask
- Image Processing: OpenCV

Technical Details

The main challenge was to improve underwater photos by fixing color and reducing noise. This involved extensive research and experimentation with various image filters using OpenCV. I read research papers, sought help online, and tested multiple filters to achieve the best results.

The filters had to balance color correction and noise reduction effectively. I adjusted the parameters of the filters and received feedback to improve them continuously. This iterative process led to the creation of filters that significantly enhance the clarity and color of underwater photos.

Contributing

1. Fork the repository.
2. Create a branch (git checkout -b feature-branch).
3. Make changes and commit (git commit -m 'Add feature').
4. Push to the branch (git push origin feature-branch).
5. Create a Pull Request.

Licensing

This project is licensed under the MIT License. See the LICENSE file for details.

About Me

I am a full-stack developer with a special interest in image processing and web applications. This project was a great learning experience, and it helped me develop my skills in image processing and web development. I enjoy solving real-world problems with technology and am always looking for new challenges.

Links

- GitHub: https://github.com/userkw
- LinkedIn: https://www.linkedin.com/in/kawthar-e-1889b9318/
- Deployed Project: https://www.youtube.com/watch?v=6QXPURvZmSg
